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

    results = []
    for match in raw_results.matches:
        meta      = match.metadata or {}
        breakdown = compute_match_breakdown(
            query=query,
            intent=intent,
            candidate_skills=meta.get("skills", []),
            candidate_location=meta.get("location"),
            candidate_exp_years=float(meta.get("experience_years") or 0),
            candidate_level=meta.get("experience_level"),
        )
        results.append({
            "candidate_id":     match.id,
            "score":            round(float(match.score) * 100),
            "name":             meta.get("name"),
            "current_role":     meta.get("current_role"),
            "current_company":  meta.get("current_company"),
            "location":         meta.get("location"),
            "experience_years": meta.get("experience_years"),
            "experience_level": meta.get("experience_level"),
            "skills":           meta.get("skills", []),
            "sources":          meta.get("sources", []),
            "candidate_bio":    meta.get("candidate_bio"),
            "fraud_risk":       meta.get("fraud_risk", "low"),
            "fraud_score":      meta.get("fraud_score", 10),
            "fraud_signals":    meta.get("fraud_signals", []),
            "match_breakdown":  breakdown,
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
