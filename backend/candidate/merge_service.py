import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select

from ai.normalize import normalize_skills
from models.candidate import Candidate


def _normalize_str(value: Any) -> str:
    return str(value or "").strip().lower()


def _merge_experience(primary_exp: list[dict] | None, secondary_exp: list[dict] | None) -> list[dict]:
    merged: list[dict] = []
    seen: set[tuple[str, str, str]] = set()

    for exp in (primary_exp or []) + (secondary_exp or []):
        if not isinstance(exp, dict):
            continue
        key = (
            _normalize_str(exp.get("company")),
            _normalize_str(exp.get("role")),
            _normalize_str(exp.get("duration")),
        )
        if key in seen:
            continue
        seen.add(key)
        merged.append(exp)
    return merged


def _merge_sources(primary_sources: list[str] | None, secondary_sources: list[str] | None) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for source in (primary_sources or []) + (secondary_sources or []):
        if not source:
            continue
        key = str(source).strip().lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append(str(source).strip())
    return merged


def _first_non_empty(primary: Any, secondary: Any) -> Any:
    if primary not in (None, "", []):
        return primary
    return secondary


def _candidate_text(candidate: Candidate) -> str:
    skills = ", ".join(candidate.skills or [])
    return " | ".join(
        [
            candidate.name or "",
            candidate.current_role or "",
            candidate.current_company or "",
            candidate.location or "",
            skills,
            candidate.candidate_bio or "",
        ]
    )


async def _reindex_candidate_async(candidate: Candidate) -> None:
    from ai.embeddings.client import get_active_index_name, get_embedding
    from search.pinecone_client import upsert_candidate

    payload = _candidate_text(candidate)
    embedding = await get_embedding(payload)
    await upsert_candidate(
        candidate_id=str(candidate.id),
        embedding=embedding,
        metadata={
            "name": candidate.name,
            "email": candidate.email,
            "location": candidate.location,
            "current_role": candidate.current_role,
            "current_company": candidate.current_company,
            "experience_years": candidate.experience_years,
            "experience_level": candidate.experience_level,
            "skills": candidate.skills or [],
            "sources": candidate.sources or [],
            "candidate_bio": candidate.candidate_bio,
            "fraud_risk": candidate.fraud_risk,
            "fraud_score": candidate.fraud_score,
            "fraud_signals": candidate.fraud_signals or [],
            "shortlisted": candidate.shortlisted,
            "status": candidate.status,
            "suggested_merge_id": candidate.suggested_merge_id,
        },
        index_name=get_active_index_name(),
    )


def _apply_merge(primary: Candidate, secondary: Candidate) -> None:
    merged_skills = normalize_skills((primary.skills or []) + (secondary.skills or []))
    merged_exp = _merge_experience(primary.all_experience, secondary.all_experience)

    primary.skills = merged_skills
    primary.all_experience = merged_exp
    primary.sources = _merge_sources(primary.sources, secondary.sources)
    primary.phone = _first_non_empty(primary.phone, secondary.phone)
    primary.location = _first_non_empty(primary.location, secondary.location)
    primary.linkedin_url = _first_non_empty(primary.linkedin_url, secondary.linkedin_url)
    primary.github_url = _first_non_empty(primary.github_url, secondary.github_url)
    primary.candidate_bio = _first_non_empty(primary.candidate_bio, secondary.candidate_bio)
    now_utc = datetime.now(timezone.utc)
    primary.updated_at = now_utc

    secondary.status = "merged"
    secondary.merged_into = str(primary.id)
    secondary.merged_by = "manual"
    secondary.updated_at = now_utc


def _reindex_candidate_sync(candidate: Candidate) -> None:
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(_reindex_candidate_async(candidate))
    finally:
        loop.close()


def merge_candidates(primary_id: str, secondary_id: str, db) -> dict:
    """
    Sync merge function used by tests and sync execution contexts.
    """
    if primary_id == secondary_id:
        raise ValueError("Cannot merge a candidate into itself")

    primary = db.execute(select(Candidate).where(Candidate.id == primary_id)).scalar_one_or_none()
    secondary = db.execute(select(Candidate).where(Candidate.id == secondary_id)).scalar_one_or_none()

    if not primary or not secondary:
        raise ValueError("Candidate not found")
    if secondary.status == "merged" and secondary.merged_into:
        raise ValueError("Secondary candidate is already merged")

    _apply_merge(primary, secondary)
    db.commit()
    db.refresh(primary)

    try:
        _reindex_candidate_sync(primary)
    except Exception:
        pass

    return {
        "ok": True,
        "primary_id": str(primary.id),
        "secondary_id": str(secondary.id),
        "skills_count": len(primary.skills or []),
        "experience_count": len(primary.all_experience or []),
    }


async def merge_candidates_async(primary_id: str, secondary_id: str, db) -> dict:
    if primary_id == secondary_id:
        raise ValueError("Cannot merge a candidate into itself")

    try:
        primary_uuid = uuid.UUID(str(primary_id))
        secondary_uuid = uuid.UUID(str(secondary_id))
    except Exception as exc:
        raise ValueError("Invalid candidate id format") from exc

    p_res = await db.execute(select(Candidate).where(Candidate.id == primary_uuid))
    s_res = await db.execute(select(Candidate).where(Candidate.id == secondary_uuid))
    primary = p_res.scalar_one_or_none()
    secondary = s_res.scalar_one_or_none()

    if not primary or not secondary:
        raise ValueError("Candidate not found")
    if secondary.status == "merged" and secondary.merged_into:
        raise ValueError("Secondary candidate is already merged")

    _apply_merge(primary, secondary)
    await db.commit()
    await db.refresh(primary)

    try:
        await _reindex_candidate_async(primary)
    except Exception:
        pass

    return {
        "ok": True,
        "primary_id": str(primary.id),
        "secondary_id": str(secondary.id),
        "skills_count": len(primary.skills or []),
        "experience_count": len(primary.all_experience or []),
    }

