"""
All REST API endpoints.

POST /api/v1/candidates/upload      — file upload → queues Celery task
POST /api/v1/search                 — semantic search with Why-This-Match breakdown
GET  /api/v1/candidates/{id}        — full candidate profile
GET  /api/v1/candidates/            — paginated candidate list
POST /api/v1/candidates/ai-summary  — lazy AI summary for popover (cache miss path)
DELETE /api/v1/candidates/{id}      — delete candidate
"""
import uuid
import json
import re
from collections import Counter
from urllib.parse import parse_qs, urlparse

import httpx
import sqlalchemy as sa
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from pydantic import BaseModel

from config import get_settings

router   = APIRouter(prefix="/api/v1")
settings = get_settings()

ALLOWED_MIME = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
ALLOWED_PIPELINE_STAGES = {"applied", "screening", "interview", "offer", "hired"}


def _parse_candidate_uuid(candidate_id: str) -> uuid.UUID:
    try:
        return uuid.UUID(candidate_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid candidate id format.") from exc


def _extract_drive_file_id(raw_link: str) -> str | None:
    parsed = urlparse(raw_link)
    query_file_id = parse_qs(parsed.query).get("id", [])
    if query_file_id:
        return query_file_id[0]

    match = re.search(r"/d/([a-zA-Z0-9_-]+)", raw_link)
    if match:
        return match.group(1)

    match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", raw_link)
    if match:
        return match.group(1)

    return None


def _filename_from_headers(content_disposition: str | None, fallback: str) -> str:
    if not content_disposition:
        return fallback

    match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^\";]+)"?', content_disposition)
    if not match:
        return fallback

    candidate_name = match.group(1).strip().strip('"')
    return candidate_name or fallback


def _normalize_source_label(raw_source: str | None) -> str:
    source = (raw_source or "").strip().lower()
    if source in {"email", "gmail_direct", "outlook"}:
        return "gmail"
    if source in {"forms", "google_forms"}:
        return "forms"
    if source in {"linkedin", "linkedin_sim"}:
        return "linkedin"
    if source:
        return source
    return "upload"


# ── File Upload ────────────────────────────────────────────────────────────────
@router.post("/candidates/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume PDF or DOCX.
    Returns task_id — subscribe to /events/{task_id} for real-time status.
    """
    if file.content_type not in ALLOWED_MIME:
        # Some clients send wrong MIME type; check extension as fallback
        fname = (file.filename or "").lower()
        if not (fname.endswith(".pdf") or fname.endswith(".docx")):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported.",
            )

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10 MB.")
    if len(file_bytes) < 100:
        raise HTTPException(status_code=400, detail="File appears to be empty.")

    from tasks.resume_tasks import parse_resume_task

    task_id = str(uuid.uuid4())
    parse_resume_task.apply_async(
        kwargs={
            "file_bytes": file_bytes,
            "mime_type":  file.content_type or "application/pdf",
            "source":     "upload",
            "filename":   file.filename or "resume",
            "metadata":   {},
        },
        task_id=task_id,
    )
    return {"task_id": task_id, "filename": file.filename, "status": "queued"}


@router.post("/integrations/google-forms")
async def ingest_google_forms_submission(payload: dict):
    """
    Receives Google Forms webhook payload and queues resume parsing.

    Expected keys: Name, Email, Resume Drive Link
    """
    name = str(payload.get("Name") or payload.get("name") or "").strip()
    email = str(payload.get("Email") or payload.get("email") or "").strip().lower()
    raw_link = str(
        payload.get("Resume Drive Link")
        or payload.get("resume_drive_link")
        or payload.get("resume_link")
        or payload.get("resume_url")
        or ""
    ).strip()

    if not raw_link:
        raise HTTPException(status_code=400, detail="Missing resume drive link in payload.")

    file_id = _extract_drive_file_id(raw_link)
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}" if file_id else raw_link

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(download_url)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to download form resume: {exc}") from exc

    if response.status_code >= 400:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to fetch resume file from provided link (status {response.status_code}).",
        )

    file_bytes = response.content
    if len(file_bytes) < 100:
        raise HTTPException(status_code=422, detail="Downloaded file appears empty.")
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10 MB.")

    fallback_name = "google_form_resume.pdf"
    if file_id:
        fallback_name = f"{file_id}.pdf"
    filename = _filename_from_headers(response.headers.get("content-disposition"), fallback_name)

    mime_type = (
        response.headers.get("content-type", "").split(";")[0].strip()
        or "application/pdf"
    )

    from tasks.resume_tasks import parse_resume_task

    task_id = str(uuid.uuid4())
    parse_resume_task.apply_async(
        kwargs={
            "file_bytes": file_bytes,
            "mime_type": mime_type,
            "source": "forms",
            "filename": filename,
            "metadata": {
                "source_system": "google_forms",
                "name": name or None,
                "email": email or None,
                "resume_drive_link": raw_link,
            },
        },
        task_id=task_id,
    )
    return {
        "status": "queued",
        "task_id": task_id,
        "source": "forms",
        "filename": filename,
    }


# ── Semantic Search ────────────────────────────────────────────────────────────
class SearchRequest(BaseModel):
    query: str
    top_k: int = 20


class MergeRequest(BaseModel):
    primary_id: str
    secondary_id: str


class CandidateStageRequest(BaseModel):
    stage: str


class CandidateNoteRequest(BaseModel):
    text: str
    author: str = "Recruiter"


@router.post("/search")
async def search_candidates(req: SearchRequest):
    """
    Natural language semantic search.
    Returns ranked candidates with pre-computed Why-This-Match breakdown.
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    if req.top_k < 1 or req.top_k > 100:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 100.")

    from search.search_svc import semantic_search

    results = await semantic_search(req.query, top_k=req.top_k)
    return {"query": req.query, "count": len(results), "results": results}


# ── Candidate List ─────────────────────────────────────────────────────────────
@router.get("/candidates/")
async def list_candidates(
    page:     int   = Query(1, ge=1),
    per_page: int   = Query(20, ge=1, le=100),
    source:   str   = Query(None),
    level:    str   = Query(None),
):
    """Paginated list of all candidates. Optionally filter by source or level."""
    from database import get_db
    from models.candidate import Candidate

    offset = (page - 1) * per_page

    async with get_db() as db:
        query = sa.select(Candidate).where(Candidate.status == "active")
        if source:
            query = query.where(Candidate.sources.contains([source]))
        if level:
            query = query.where(Candidate.experience_level == level)

        total_result  = await db.execute(sa.select(sa.func.count()).select_from(query.subquery()))
        total         = total_result.scalar()

        result        = await db.execute(
            query.order_by(Candidate.created_at.desc()).offset(offset).limit(per_page)
        )
        candidates    = result.scalars().all()

    return {
        "total":    total,
        "page":     page,
        "per_page": per_page,
        "items":    [_serialize_candidate(c) for c in candidates],
    }


@router.get("/ui/sidebar-summary")
async def get_sidebar_summary():
    """Aggregated metrics for premium sidebar badges and quick insights."""
    from database import get_db
    from models.candidate import Candidate

    async with get_db() as db:
        total_result = await db.execute(
            sa.select(sa.func.count()).select_from(
                sa.select(Candidate.id).where(Candidate.status == "active").subquery()
            )
        )
        total_candidates = int(total_result.scalar() or 0)

        shortlisted_result = await db.execute(
            sa.select(sa.func.count()).select_from(
                sa.select(Candidate.id)
                .where(Candidate.status == "active", Candidate.shortlisted.is_(True))
                .subquery()
            )
        )
        shortlisted = int(shortlisted_result.scalar() or 0)

        high_risk_result = await db.execute(
            sa.select(sa.func.count()).select_from(
                sa.select(Candidate.id)
                .where(Candidate.status == "active", Candidate.fraud_risk == "high")
                .subquery()
            )
        )
        high_risk = int(high_risk_result.scalar() or 0)

        stage_rows = await db.execute(
            sa.select(Candidate.pipeline_stage, sa.func.count())
            .where(Candidate.status == "active")
            .group_by(Candidate.pipeline_stage)
        )

        source_rows = await db.execute(
            sa.select(Candidate.sources).where(Candidate.status == "active")
        )

    stage_counts = {
        str(stage or "unknown").lower(): int(count or 0)
        for stage, count in stage_rows.all()
    }

    source_counter: Counter[str] = Counter()
    for sources in source_rows.scalars().all():
        if not isinstance(sources, list):
            continue
        for source in sources:
            normalized = _normalize_source_label(source if isinstance(source, str) else str(source))
            source_counter[normalized] += 1

    for label in ("gmail", "forms", "linkedin", "hrms", "upload"):
        source_counter.setdefault(label, 0)

    connected_sources = sum(
        1 for label in ("gmail", "forms", "linkedin", "hrms", "upload") if source_counter[label] > 0
    )

    return {
        "total_candidates": total_candidates,
        "shortlisted": shortlisted,
        "high_risk": high_risk,
        "connected_sources": connected_sources,
        "stage_counts": stage_counts,
        "source_counts": dict(source_counter),
    }


@router.post("/candidates/merge")
async def merge_candidates_endpoint(req: MergeRequest):
    from candidate.merge_service import merge_candidates_async
    from database import get_db

    async with get_db() as db:
        try:
            result = await merge_candidates_async(req.primary_id, req.secondary_id, db)
        except ValueError as exc:
            detail = str(exc)
            status_code = 409 if "already merged" in detail.lower() else 400
            raise HTTPException(status_code=status_code, detail=detail) from exc
    return result


@router.patch("/candidates/{candidate_id}/stage")
async def update_candidate_stage(candidate_id: str, req: CandidateStageRequest):
    from database import get_db
    from models.candidate import Candidate

    normalized_stage = req.stage.strip().lower()
    if normalized_stage not in ALLOWED_PIPELINE_STAGES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid stage. Allowed values: Applied, Screening, Interview, Offer, Hired."
            ),
        )

    candidate_uuid = _parse_candidate_uuid(candidate_id)

    async with get_db() as db:
        result = await db.execute(sa.select(Candidate).where(Candidate.id == candidate_uuid))
        candidate = result.scalars().first()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found.")

        candidate.pipeline_stage = normalized_stage
        await db.flush()
        await db.refresh(candidate)

    return {
        "candidate_id": str(candidate.id),
        "pipeline_stage": candidate.pipeline_stage,
        "status": "updated",
    }


@router.get("/candidates/{candidate_id}/notes")
async def list_candidate_notes(candidate_id: str):
    from database import get_db
    from models.candidate import Candidate
    from models.candidate_note import CandidateNote

    candidate_uuid = _parse_candidate_uuid(candidate_id)

    async with get_db() as db:
        candidate_result = await db.execute(
            sa.select(Candidate.id).where(Candidate.id == candidate_uuid)
        )
        if not candidate_result.scalar():
            raise HTTPException(status_code=404, detail="Candidate not found.")

        notes_result = await db.execute(
            sa.select(CandidateNote)
            .where(CandidateNote.candidate_id == candidate_uuid)
            .order_by(CandidateNote.created_at.desc())
        )
        notes = notes_result.scalars().all()

    return {
        "items": [
            {
                "id": str(note.id),
                "candidate_id": str(note.candidate_id),
                "text": note.text,
                "author": note.author,
                "created_at": note.created_at.isoformat() if note.created_at else None,
            }
            for note in notes
        ]
    }


@router.post("/candidates/{candidate_id}/notes")
async def add_candidate_note(candidate_id: str, req: CandidateNoteRequest):
    from database import get_db
    from models.candidate import Candidate
    from models.candidate_note import CandidateNote

    clean_text = req.text.strip()
    if not clean_text:
        raise HTTPException(status_code=400, detail="Note text cannot be empty.")

    candidate_uuid = _parse_candidate_uuid(candidate_id)

    async with get_db() as db:
        candidate_result = await db.execute(
            sa.select(Candidate.id).where(Candidate.id == candidate_uuid)
        )
        if not candidate_result.scalar():
            raise HTTPException(status_code=404, detail="Candidate not found.")

        note = CandidateNote(
            candidate_id=candidate_uuid,
            text=clean_text,
            author=req.author.strip() or "Recruiter",
        )
        db.add(note)
        await db.flush()
        await db.refresh(note)

    return {
        "id": str(note.id),
        "candidate_id": str(note.candidate_id),
        "text": note.text,
        "author": note.author,
        "created_at": note.created_at.isoformat() if note.created_at else None,
    }


@router.get("/integrations/inbound-feed")
async def list_inbound_feed(limit: int = Query(20, ge=1, le=100)):
    import redis as redis_lib

    try:
        redis_client = redis_lib.from_url(settings.redis_url, decode_responses=True)
        cursor = 0
        entries: list[dict] = []

        while True:
            cursor, keys = redis_client.scan(cursor=cursor, match="task_status:*", count=200)
            for key in keys:
                raw = redis_client.get(key)
                if not raw:
                    continue
                payload = json.loads(raw)
                if not isinstance(payload, dict):
                    continue
                payload["task_id"] = key.replace("task_status:", "", 1)
                entries.append(payload)
            if cursor == 0:
                break
    except redis_lib.exceptions.RedisError as exc:
        raise HTTPException(status_code=503, detail=f"Redis unavailable: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid task status payload: {exc}") from exc

    entries.sort(key=lambda item: float(item.get("ts", 0) or 0), reverse=True)
    return {"items": entries[:limit], "count": min(limit, len(entries))}


# ── Candidate Detail ───────────────────────────────────────────────────────────
@router.get("/candidates/{candidate_id}")
async def get_candidate(candidate_id: str):
    """Full candidate profile including all parsed fields."""
    from database import get_db
    from models.candidate import Candidate
    candidate_uuid = _parse_candidate_uuid(candidate_id)

    async with get_db() as db:
        result    = await db.execute(
            sa.select(Candidate).where(Candidate.id == candidate_uuid)
        )
        candidate = result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    return _serialize_candidate(candidate)


# ── Delete Candidate ───────────────────────────────────────────────────────────
@router.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: str):
    """Delete candidate from PostgreSQL and Pinecone."""
    from database import get_db
    from models.candidate import Candidate
    from search.pinecone_client import delete_candidate as pinecone_delete
    candidate_uuid = _parse_candidate_uuid(candidate_id)

    async with get_db() as db:
        result    = await db.execute(
            sa.select(Candidate).where(Candidate.id == candidate_uuid)
        )
        candidate = result.scalars().first()

        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found.")

        await db.delete(candidate)

    await pinecone_delete(candidate_id, index_name=candidate.pinecone_index)
    return {"deleted": True, "candidate_id": candidate_id}


# ── Lazy AI Summary (Why-This-Match popover) ───────────────────────────────────
class AISummaryRequest(BaseModel):
    candidate_id: str
    query:        str


@router.post("/candidates/ai-summary")
async def generate_ai_summary(req: AISummaryRequest):
    """
    Generates ai_summary text for the Why-This-Match popover.
    Called ONLY when ai_summary is None (cache miss on popover open).
    Uses Claude Haiku — ~$0.000050 per call.
    """
    import anthropic
    from database import get_db
    from models.candidate import Candidate
    candidate_uuid = _parse_candidate_uuid(req.candidate_id)

    async with get_db() as db:
        result    = await db.execute(
            sa.select(Candidate).where(Candidate.id == candidate_uuid)
        )
        candidate = result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    prompt = (
        f'Recruiter query: "{req.query}"\n\n'
        f"Candidate: {candidate.name}, {candidate.current_role} at {candidate.current_company}\n"
        f"Skills: {', '.join((candidate.skills or [])[:15])}\n"
        f"Experience: {candidate.experience_years} years ({candidate.experience_level})\n"
        f"Bio: {candidate.candidate_bio}\n\n"
        "Write 1-2 sentences explaining why this candidate matches the query. "
        "Be specific — name matching skills. Note gaps if any. Max 40 words."
    )

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=80,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"ai_summary": message.content[0].text.strip()}


# ── Serializer helper ──────────────────────────────────────────────────────────
def _serialize_candidate(c) -> dict:
    return {
        "id":                str(c.id),
        "name":              c.name,
        "email":             c.email,
        "phone":             c.phone,
        "location":          c.location,
        "linkedin_url":      c.linkedin_url,
        "github_url":        c.github_url,
        "current_role":      c.current_role,
        "current_company":   c.current_company,
        "experience_years":  c.experience_years,
        "experience_level":  c.experience_level,
        "skills":            c.skills,
        "all_experience":    c.all_experience,
        "certifications":    c.certifications,
        "candidate_bio":     c.candidate_bio,
        "sources":           c.sources,
        "ai_score":          getattr(c, "ai_score", 0),
        "pipeline_stage":    getattr(c, "pipeline_stage", "applied"),
        "status":            getattr(c, "status", "active"),
        "shortlisted":       getattr(c, "shortlisted", False),
        "shortlist_rule_id": getattr(c, "shortlist_rule_id", None),
        "fraud_risk":        getattr(c, "fraud_risk", "low"),
        "fraud_score":       getattr(c, "fraud_score", 10),
        "fraud_signals":     getattr(c, "fraud_signals", []),
        "suggested_merge_id": getattr(c, "suggested_merge_id", None),
        "parse_quality":     c.parse_quality,
        "github_enrichment": c.github_enrichment,
        "created_at":        c.created_at.isoformat() if c.created_at else None,
    }
