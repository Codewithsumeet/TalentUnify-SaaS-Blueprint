"""
Celery pipeline orchestrator.

Full sequence: Tier 0 → 1 → 2A → EARLY EMAIL DEDUP → 2B → 2C → 3 → 4 → 5A → 5B → GitHub

BUG FIX 10: DB-level race condition guard via IntegrityError catch.
BUG FIX 11: asyncio.wait_for(timeout=45) on extract_to_markdown.
"""
import asyncio
import json
import time
import uuid
from typing import Callable

from .celery_app import celery_app
from config import get_settings

settings = get_settings()
_distance_impl: Callable[[str, str], int] | None = None


def _fallback_levenshtein(left: str, right: str) -> int:
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)

    if len(left) < len(right):
        left, right = right, left

    previous_row = list(range(len(right) + 1))
    for i, left_char in enumerate(left, start=1):
        current_row = [i]
        for j, right_char in enumerate(right, start=1):
            insert_cost = previous_row[j] + 1
            delete_cost = current_row[j - 1] + 1
            replace_cost = previous_row[j - 1] + (left_char != right_char)
            current_row.append(min(insert_cost, delete_cost, replace_cost))
        previous_row = current_row

    return previous_row[-1]


def _distance(left: str, right: str) -> int:
    global _distance_impl
    if _distance_impl is None:
        try:
            from Levenshtein import distance as levenshtein_distance

            _distance_impl = levenshtein_distance
        except Exception:
            _distance_impl = _fallback_levenshtein
    return _distance_impl(left, right)


def _run(coro):
    """Run async coroutine from sync Celery context. Uses asyncio.run() for Py 3.11+."""
    return asyncio.run(coro)


def _push(task_id: str, status: str, extra: dict | None = None) -> None:
    """Write task status to Redis for SSE endpoint to stream to frontend."""
    import redis
    r       = redis.from_url(settings.redis_url)
    payload = {"status": status, "ts": time.time(), **(extra or {})}
    r.setex(f"task_status:{task_id}", 300, json.dumps(payload))


def _email_exists(email: str) -> str | None:
    """Returns existing candidate_id if email found, else None."""
    import sqlalchemy as sa
    from database import get_db_session as get_sync_db
    from models.candidate import Candidate

    with get_sync_db() as db:
        row = db.execute(
            sa.select(Candidate.id).where(
                Candidate.email == email.lower().strip()
            )
        ).first()
        return str(row[0]) if row else None


@celery_app.task(bind=True, max_retries=2, default_retry_delay=5)
def parse_resume(
    self,
    file_bytes: bytes,
    mime_type:  str,
    source:     str,
    filename:   str,
    metadata:   dict | None = None,
) -> dict:
    """Full resume processing pipeline. Called by upload endpoint and Gmail webhook."""
    tid      = self.request.id
    metadata = metadata or {}
    status_base = {"source": source, "filename": filename}

    def push(status: str, extra: dict | None = None) -> None:
        payload = dict(status_base)
        if extra:
            payload.update(extra)
        _push(tid, status, payload)

    try:
        import sqlalchemy as sa
        from sqlalchemy.exc import IntegrityError
        from database import get_db_session as get_sync_db
        from models.candidate import Candidate
        from ai.preproc import preprocess_file as validate_file, quick_extract_contacts as regex_contacts
        from ai.extractor import extract_to_markdown, _extract_raw_text
        from ai.nlp.bert_ner_fallback import extract_contact_entities_with_fallback as extract_contacts
        from ai.skill_extractor import extract_skills
        from ai.tier3_llm_enrichment import enrich
        from ai.normalize import normalize_and_assess
        from ai.embeddings.chunker import get_aggregate_embedding as aggregate_embedding
        from search.pinecone_client import (
            active_index,
            upsert as pinecone_upsert,
            query as pinecone_query,
        )

        # ── Tier 0: Pre-processing ────────────────────────────────────────────
        pre = validate_file(file_bytes, mime_type, filename)
        if not pre["ok"]:
            push("failed", {"reason": pre["error"]})
            return {"status": "failed", "reason": pre["error"]}

        push("parsing", {"step": "extracting"})

        # ── Tier 1: Document → Markdown (BUG FIX 11: 45s timeout) ────────────
        try:
            ext = _run(
                asyncio.wait_for(
                    extract_to_markdown(file_bytes, pre["mime_type"]),
                    timeout=45.0,
                )
            )
        except asyncio.TimeoutError:
            # LlamaParse timed out — drop to emergency pypdf fallback directly
            raw_text = _extract_raw_text(file_bytes, pre["mime_type"])
            ext = {
                "markdown": raw_text or "(timeout_fallback)",
                "quality":  "low",
                "parser":   "timeout_fallback",
            }

        md = ext["markdown"]
        if not md or md in ("(parse_failed)", "(timeout_fallback)"):
            push("failed", {"reason": "empty_document"})
            return {"status": "failed", "reason": "empty_document"}

        # ── Tier 2A: Contact NER ──────────────────────────────────────────────
        push("parsing", {"step": "extracting_contacts"})
        contacts = extract_contacts(md)
        regex    = regex_contacts(md)
        for k in ("email", "phone", "linkedin_url", "github_url"):
            if regex.get(k) and not contacts.get(k):
                contacts[k] = regex[k]

        # ── EARLY EMAIL DEDUP — skip LLM if already in DB ────────────────────
        if contacts.get("email"):
            existing = _email_exists(contacts["email"])
            if existing:
                push("duplicate", {"existing_id": existing})
                return {"status": "duplicate", "existing_id": existing}

        # ── Tier 2B: Skill extraction ─────────────────────────────────────────
        push("parsing", {"step": "extracting_skills"})
        contacts["skills_phase2"] = extract_skills(md)

        # ── Tier 3: LLM enrichment (Claude 3.5 Haiku) ────────────────────────
        push("parsing", {"step": "enriching"})
        enriched = _run(enrich(md, contacts))

        # ── Tier 4: Skill normalization + fraud assessment ───────────────────
        all_skills = list(set(
            (enriched.get("skills") or []) +
            contacts.get("skills_phase2", []) +
            contacts.get("skills_bert", [])
        ))
        enriched["skills"] = all_skills
        enriched["raw_text"] = md
        enriched = normalize_and_assess(enriched)

        # ── Tier 5A: Embedding + full deduplication ───────────────────────────
        push("parsing", {"step": "deduplicating"})
        embedding = _run(aggregate_embedding(md))

        # L1: email (post-enrichment, may differ from pre-NER email)
        if enriched.get("email"):
            existing = _email_exists(enriched["email"])
            if existing:
                push("duplicate", {"existing_id": existing})
                return {"status": "duplicate", "existing_id": existing}

        # L2: Levenshtein fuzzy name match
        if enriched.get("name") and len(enriched["name"].strip()) > 2:
            with get_sync_db() as db:
                rows = db.execute(sa.select(Candidate.id, Candidate.name)).all()
            name_clean = enriched["name"].lower().strip()
            for cid, cname in rows:
                if cname and _distance(name_clean, cname.lower().strip()) <= 2:
                    push("duplicate", {"existing_id": str(cid)})
                    return {"status": "duplicate", "existing_id": str(cid)}

        # L3: Pinecone vector cosine similarity > 0.92
        try:
            res = _run(pinecone_query(vector=embedding, top_k=1))
            if res.matches and float(res.matches[0].score) > 0.92:
                push("duplicate", {"existing_id": res.matches[0].id})
                return {"status": "duplicate", "existing_id": res.matches[0].id}
        except Exception:
            pass  # dedup failure is non-fatal

        # ── Tier 5B: Write to PostgreSQL + Pinecone ───────────────────────────
        push("parsing", {"step": "saving"})
        candidate_id = str(uuid.uuid4())
        idx_name     = active_index()

        try:
            with get_sync_db() as db:
                candidate = Candidate(
                    id               = candidate_id,
                    name             = enriched.get("name"),
                    email            = enriched.get("email"),
                    phone            = enriched.get("phone"),
                    location         = enriched.get("location"),
                    linkedin_url     = enriched.get("linkedin_url"),
                    github_url       = enriched.get("github_url"),
                    current_role     = enriched.get("current_role"),
                    current_company  = enriched.get("current_company"),
                    experience_years = enriched.get("experience_years"),
                    experience_level = enriched.get("experience_level"),
                    skills           = enriched.get("skills", []),
                    all_experience   = enriched.get("all_experience", []),
                    certifications   = enriched.get("certifications", []),
                    candidate_bio    = enriched.get("candidate_bio"),
                    sources          = [source],
                    parse_quality    = ext["quality"],
                    pinecone_index   = idx_name,
                    fraud_risk       = enriched.get("fraud_risk", "low"),
                    fraud_score      = enriched.get("fraud_score", 10),
                    fraud_signals    = enriched.get("fraud_signals", []),
                    status           = "active",
                )
                db.add(candidate)
                db.commit()

        except IntegrityError:
            # BUG FIX 10: Concurrent workers hit the UNIQUE constraint on email.
            # One wins (already committed above) — this worker treats it as a duplicate.
            with get_sync_db() as db:
                row = db.execute(
                    sa.select(Candidate.id).where(
                        Candidate.email == enriched.get("email")
                    )
                ).first()
            existing_id = str(row[0]) if row else "unknown"
            push("duplicate", {"existing_id": existing_id, "reason": "concurrent_insert"})
            return {"status": "duplicate", "existing_id": existing_id}

        # Pinecone upsert (non-blocking on failure — DB write already succeeded)
        try:
            _run(pinecone_upsert(
                candidate_id = candidate_id,
                embedding    = embedding,
                metadata     = {
                    "name":             enriched.get("name"),
                    "email":            enriched.get("email"),
                    "location":         enriched.get("location"),
                    "current_role":     enriched.get("current_role"),
                    "current_company":  enriched.get("current_company"),
                    "experience_years": enriched.get("experience_years"),
                    "experience_level": enriched.get("experience_level"),
                    "skills":           enriched.get("skills", []),
                    "sources":          [source],
                    "candidate_bio":    enriched.get("candidate_bio"),
                    "fraud_risk":       enriched.get("fraud_risk", "low"),
                    "fraud_score":      enriched.get("fraud_score", 10),
                    "fraud_signals":    enriched.get("fraud_signals", []),
                },
                index_name = idx_name,
            ))
        except Exception as pinecone_err:
            # Pinecone failure does NOT roll back the PostgreSQL write.
            # Candidate is in the DB. Vector search won't find them until re-indexed.
            push("complete", {
                "candidate_id":  candidate_id,
                "warning":       f"Pinecone upsert failed: {pinecone_err}",
            })

        # GitHub enrichment (optional, async, non-blocking)
        if enriched.get("github_url"):
            from tasks.github_tasks import enrich_github
            enrich_github.delay(candidate_id, enriched["github_url"])

        result = {
            "status":        "complete",
            "candidate_id":  candidate_id,
            "name":          enriched.get("name"),
            "skills_count":  len(enriched.get("skills", [])),
            "parse_quality": ext["quality"],
            "fraud_risk":    enriched.get("fraud_risk", "low"),
        }
        push("complete", result)
        return result

    except Exception as exc:
        push("failed", {"reason": str(exc)})
        raise self.retry(exc=exc, countdown=5)


# Backward-compatible task name expected by existing API routes
parse_resume_task = parse_resume
