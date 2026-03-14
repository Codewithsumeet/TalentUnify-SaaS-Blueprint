"""
Main semantic search service.
Pattern: KarthikAlagarsamy/Resume-Semantic-Search adapted for Pinecone ANN.

Flow:
  1. Parse intent from NL query (location, level, remote)
  2. Embed query with same model as candidates
  3. ANN search in Pinecone with optional metadata pre-filters
  4. Pre-compute Why-This-Match breakdown per result
  5. Return ranked list sorted by score desc
"""
import uuid

import sqlalchemy as sa

from database import get_db
from models.candidate import Candidate
from search.pinecone_client import query_index
from search.match_scorer import compute_match_breakdown
from ai.embeddings.client import get_embedding

LOCATION_HINTS = ["in ", "at ", "from ", "based in ", "located in ", "near "]
LEVEL_HINTS    = {
    "senior":    "Senior",
    "junior":    "Junior",
    "mid":       "Mid",
    "lead":      "Senior",
    "principal": "Principal",
    "fresher":   "Fresher",
    "entry":     "Fresher",
    "associate": "Junior",
    "staff":     "Principal",
}


def _parse_candidate_uuid(raw_id: str) -> uuid.UUID | None:
    try:
        return uuid.UUID(str(raw_id))
    except Exception:
        return None


async def _load_candidates(candidate_ids: list[str]) -> dict[str, Candidate]:
    parsed_ids = [_parse_candidate_uuid(candidate_id) for candidate_id in candidate_ids]
    valid_ids = [candidate_id for candidate_id in parsed_ids if candidate_id is not None]
    if not valid_ids:
        return {}

    async with get_db() as db:
        result = await db.execute(
            sa.select(Candidate).where(
                Candidate.id.in_(valid_ids),  # type: ignore[arg-type]
                Candidate.status == "active",
            )
        )
        candidates = result.scalars().all()

    return {str(candidate.id): candidate for candidate in candidates}


def parse_query_intent(query: str) -> dict:
    """Extracts structured intent from a natural language recruiter query."""
    q = query.lower()

    location = None
    for hint in LOCATION_HINTS:
        if hint in q:
            after    = q.split(hint, 1)[1]
            location = after.split()[0].strip(".,;()").title()
            break

    level  = next((v for k, v in LEVEL_HINTS.items() if k in q), None)
    remote = any(w in q for w in ["remote", "wfh", "work from home", "distributed", "anywhere"])

    return {
        "raw_query": query,
        "location":  location,
        "level":     level,
        "remote":    remote,
    }


async def semantic_search(query: str, top_k: int = 20) -> list[dict]:
    """
    Main search entry point.
    Returns list of result dicts, sorted by score descending.
    """
    intent          = parse_query_intent(query)
    query_embedding = await get_embedding(query)

    # Build metadata pre-filter (reduces ANN search space)
    filters: dict = {}
    if intent["location"]:
        filters["location"] = {"$contains": intent["location"]}
    if intent["level"]:
        filters["experience_level"] = {"$eq": intent["level"]}

    raw_results = await query_index(
        vector=query_embedding,
        top_k=top_k,
        filter=filters if filters else None,
    )

    candidate_records = await _load_candidates([str(match.id) for match in raw_results.matches])

    results = []
    for match in raw_results.matches:
        candidate_id = str(match.id)
        meta = match.metadata or {}
        candidate = candidate_records.get(candidate_id)

        candidate_skills = list(candidate.skills or []) if candidate else list(meta.get("skills", []))
        candidate_location = candidate.location if candidate else meta.get("location")
        candidate_exp_years = float(candidate.experience_years or 0) if candidate else float(meta.get("experience_years") or 0)
        candidate_level = candidate.experience_level if candidate else meta.get("experience_level")
        breakdown = compute_match_breakdown(
            query=query,
            intent=intent,
            candidate_skills=candidate_skills,
            candidate_location=candidate_location,
            candidate_exp_years=candidate_exp_years,
            candidate_level=candidate_level,
        )
        results.append({
            "candidate_id": candidate_id,
            "score": round(float(match.score) * 100),
            "name": candidate.name if candidate else meta.get("name"),
            "current_role": candidate.current_role if candidate else meta.get("current_role"),
            "current_company": candidate.current_company if candidate else meta.get("current_company"),
            "location": candidate_location,
            "experience_years": candidate.experience_years if candidate else meta.get("experience_years"),
            "experience_level": candidate_level,
            "skills": candidate_skills,
            "sources": list(candidate.sources or []) if candidate else list(meta.get("sources", [])),
            "candidate_bio": candidate.candidate_bio if candidate else meta.get("candidate_bio"),
            "fraud_risk": candidate.fraud_risk if candidate else meta.get("fraud_risk", "low"),
            "fraud_score": candidate.fraud_score if candidate else meta.get("fraud_score", 10),
            "fraud_signals": list(candidate.fraud_signals or []) if candidate else list(meta.get("fraud_signals", [])),
            "match_breakdown": breakdown,
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
