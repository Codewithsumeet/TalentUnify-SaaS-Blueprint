from dataclasses import dataclass
from typing import Any


@dataclass
class ShortlistRuleConfig:
    id: str
    name: str
    role_target: str = ""
    min_score: int = 70
    required_skills: list[str] | None = None
    any_of_skills: list[str] | None = None
    min_experience_years: float = 0.0
    location_filter: str | None = None
    level_filter: list[str] | None = None
    auto_apply: bool = False
    priority: int = 0


WEIGHTS = {
    "ai_score": 0.40,
    "required_skills": 0.25,
    "any_of_skills": 0.12,
    "experience": 0.15,
    "location": 0.08,
}


def _to_set(values: list[str] | None) -> set[str]:
    return {str(value).strip().lower() for value in (values or []) if str(value).strip()}


def _location_score(candidate_location: str | None, rule_location: str | None) -> float:
    if not rule_location:
        return 1.0
    cand = (candidate_location or "").strip().lower()
    target = rule_location.strip().lower()
    if not cand:
        return 0.40
    return 1.0 if target in cand else 0.40


def evaluate_candidate(candidate: dict[str, Any], rule: ShortlistRuleConfig) -> dict[str, Any]:
    candidate_ai = float(candidate.get("ai_score") or candidate.get("aiScore") or 0)
    ai_score_component = max(0.0, min(1.0, candidate_ai / 100.0))

    candidate_skills = _to_set(candidate.get("skills"))
    required_skills = _to_set(rule.required_skills)
    any_skills = _to_set(rule.any_of_skills)

    missing_required = sorted(required_skills - candidate_skills)
    required_ok = not missing_required
    required_component = 1.0 if required_ok else 0.0

    any_component = 1.0
    if any_skills:
        matched_any = len(candidate_skills & any_skills)
        any_component = matched_any / max(1, len(any_skills))

    years = float(candidate.get("experience_years") or 0)
    min_years = float(rule.min_experience_years or 0)
    if min_years <= 0:
        experience_component = 1.0
    else:
        experience_component = max(0.0, min(1.0, years / min_years))

    location_component = _location_score(
        candidate_location=str(candidate.get("location") or ""),
        rule_location=rule.location_filter,
    )

    weighted = (
        ai_score_component * WEIGHTS["ai_score"]
        + required_component * WEIGHTS["required_skills"]
        + any_component * WEIGHTS["any_of_skills"]
        + experience_component * WEIGHTS["experience"]
        + location_component * WEIGHTS["location"]
    )
    rule_score = round(weighted * 100, 2)

    matches = required_ok and (rule_score >= float(rule.min_score))

    return {
        "rule_id": rule.id,
        "rule_name": rule.name,
        "priority": rule.priority,
        "rule_score": rule_score,
        "matches": matches,
        "auto_shortlist": bool(matches and rule.auto_apply),
        "component_scores": {
            "ai_score": round(ai_score_component, 2),
            "required_skills": round(required_component, 2),
            "any_of_skills": round(any_component, 2),
            "experience": round(experience_component, 2),
            "location": round(location_component, 2),
        },
        "missing_required_skills": missing_required,
    }


def run_all_rules(candidate: dict[str, Any], rules: list[ShortlistRuleConfig]) -> list[dict[str, Any]]:
    ordered = sorted(rules, key=lambda item: item.priority, reverse=True)
    results = [evaluate_candidate(candidate, rule) for rule in ordered]

    auto_locked = False
    for result, rule in zip(results, ordered):
        should_auto = bool(result["matches"] and rule.auto_apply and not auto_locked)
        result["auto_shortlist"] = should_auto
        if should_auto:
            auto_locked = True

    return results

