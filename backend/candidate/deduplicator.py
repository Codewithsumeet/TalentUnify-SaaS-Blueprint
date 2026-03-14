"""
Three-level deduplication before DB write.

L1: SQL exact email match      — 1ms, most reliable
L2: Levenshtein fuzzy name     — ~10ms, catches typos and format variants
L3: Pinecone cosine > 0.92     — catches duplicates with different emails/names

Stops at first match (does not continue to L3 if L1 matches).
Returns candidate_id if duplicate found, None if new candidate.
"""
from Levenshtein import distance as levenshtein_distance
from search.pinecone_client import query_index
import sqlalchemy as sa


async def find_duplicate(
    email:      str | None,
    name:       str | None,
    embedding:  list[float],
    db_session,
) -> str | None:
    """
    Returns existing candidate_id string if a duplicate is found.
    Returns None if this is a new candidate.

    db_session must be a SQLAlchemy Session (sync) — called from Celery task context.
    """
    from models.candidate import Candidate

    # ── L1: Exact email match ─────────────────────────────────────────────────
    if email:
        row = db_session.execute(
            sa.select(Candidate.id).where(Candidate.email == email.lower().strip())
        ).first()
        if row:
            return str(row[0])

    # ── L2: Fuzzy name match (Levenshtein ≤ 2) ────────────────────────────────
    if name and len(name.strip()) > 2:
        all_rows = db_session.execute(
            sa.select(Candidate.id, Candidate.name)
        ).all()
        name_clean = name.lower().strip()
        for cand_id, cand_name in all_rows:
            if cand_name and levenshtein_distance(name_clean, cand_name.lower().strip()) <= 2:
                return str(cand_id)

    # ── L3: Pinecone cosine similarity > 0.92 ─────────────────────────────────
    try:
        results = await query_index(vector=embedding, top_k=1)
        if results.matches and float(results.matches[0].score) > 0.92:
            return str(results.matches[0].id)
    except Exception:
        pass  # dedup failure is non-fatal — better to create a duplicate than crash

    return None
