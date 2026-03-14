"""
Tier 4: Skill normalization.
Applies skills_canonical.json alias map to deduplicate and normalize skill names.
Pure Python. No model. Always runs after Tier 3, before DB write.

"ReactJS" → "React", "NodeJS" → "Node.js", "k8s" → "Kubernetes"
"""
import json
from functools import lru_cache
from pathlib import Path

from .fraud_detector import detect_fraud

@lru_cache(maxsize=1)
def _get_alias_map() -> dict[str, str]:
    data = json.loads(Path("data/skills_canonical.json").read_text())
    alias_map: dict[str, str] = {}
    for canonical, aliases in data.items():
        alias_map[canonical.lower()] = canonical
        for alias in aliases:
            alias_map[alias.lower()] = canonical
    return alias_map


def normalize_skill(raw: str) -> str:
    """Normalize a single skill string to its canonical form."""
    return _get_alias_map().get(raw.lower().strip(), raw.strip())


def normalize_skills(skills: list[str]) -> list[str]:
    """
    Normalize and deduplicate a list of skill strings.
    Preserves order of first occurrence.
    """
    seen:   set[str]  = set()
    result: list[str] = []
    for s in skills:
        if not s or not s.strip():
            continue
        norm = normalize_skill(s)
        key  = norm.lower()
        if key not in seen:
            seen.add(key)
            result.append(norm)
    return result


def normalize_and_assess(candidate: dict) -> dict:
    """
    Tier 4 post-processing.
    Runs skill normalization and then fraud detection enrichment.
    """
    candidate["skills"] = normalize_skills(candidate.get("skills") or [])
    candidate.update(detect_fraud(candidate))
    return candidate
