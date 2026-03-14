"""
Pre-computes the "Why This Match?" breakdown at search time.
Zero additional latency on popover open — everything is calculated here.

Weights: skills 50%, experience 25%, location 15%, remote 10%.
Output schema modelled on LlamaFactoryAI/cv-job-description-matching.
"""
import json
from functools import lru_cache
from pathlib import Path

WEIGHTS = {
    "skills":     0.50,
    "experience": 0.25,
    "location":   0.15,
    "remote":     0.10,
}

LEVEL_ORDER = {
    "Fresher":   0,
    "Junior":    1,
    "Mid":       2,
    "Senior":    3,
    "Principal": 4,
}


@lru_cache(maxsize=1)
def _get_canonical_names() -> list[str]:
    return list(json.loads(Path("data/skills_canonical.json").read_text()).keys())


def compute_match_breakdown(
    query:               str,
    intent:              dict,
    candidate_skills:    list[str],
    candidate_location:  str | None,
    candidate_exp_years: float,
    candidate_level:     str | None,
) -> dict:
    """
    Returns full match breakdown dict. All fields are deterministic.
    ai_summary is always None here — filled lazily on popover open by Claude Haiku.
    """
    canonical_names     = _get_canonical_names()
    query_lower         = query.lower()
    query_skills        = [s for s in canonical_names if s.lower() in query_lower]
    candidate_skill_set = {s.lower() for s in candidate_skills}

    matched_skills = [s for s in query_skills if s.lower() in candidate_skill_set]
    missing_skills = [s for s in query_skills if s.lower() not in candidate_skill_set]
    bonus_skills   = [
        s for s in candidate_skills
        if s.lower() not in {q.lower() for q in query_skills}
    ][:3]
    skill_score = len(matched_skills) / max(len(query_skills), 1)

    # Experience score
    req_level  = intent.get("level")
    cand_level = candidate_level
    if req_level and cand_level:
        req_ord  = LEVEL_ORDER.get(req_level, 2)
        cand_ord = LEVEL_ORDER.get(cand_level, 2)
        exp_score = 1.0 if cand_ord >= req_ord else max(0.3, 1.0 - (req_ord - cand_ord) * 0.25)
    else:
        exp_score = 0.8  # no level requirement stated

    # Location score
    location_pct = 80  # default: no location requirement
    if intent.get("location") and candidate_location:
        location_pct = 100 if intent["location"].lower() in candidate_location.lower() else 0

    # Remote score
    remote_score = 1.0 if intent.get("remote") else 0.8

    weighted = (
        skill_score          * WEIGHTS["skills"]     +
        exp_score            * WEIGHTS["experience"] +
        (location_pct / 100) * WEIGHTS["location"]   +
        remote_score         * WEIGHTS["remote"]
    )
    final_score = round(weighted * 100)
    match_level = (
        "Strong"  if final_score >= 80 else
        "Good"    if final_score >= 65 else
        "Partial" if final_score >= 45 else
        "Weak"
    )

    return {
        "overall_score": final_score,
        "match_level":   match_level,
        "skill_analysis": {
            "matched":   matched_skills,
            "missing":   missing_skills,
            "bonus":     bonus_skills,
            "match_pct": round(skill_score * 100),
        },
        "experience_analysis": {
            "candidate_years": candidate_exp_years,
            "candidate_level": candidate_level,
            "required_level":  req_level,
            "level_match":     (cand_ord >= req_ord) if (req_level and cand_level) else None,
            "delta": (
                f"+{int(candidate_exp_years - 3)}yr"
                if (candidate_exp_years or 0) > 3
                else "entry level"
            ),
        },
        "location_analysis": {
            "candidate":   candidate_location,
            "required":    intent.get("location"),
            "match_pct":   location_pct,
            "remote_open": intent.get("remote", False),
        },
        "ai_summary": None,
    }
