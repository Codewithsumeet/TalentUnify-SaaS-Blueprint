"""
Tier 2B: Two-phase skill extraction.

Phase 1: keyword scan against skills_canonical.json (1ms, free)
Phase 2: facebook/bart-large-mnli zero-shot classification
         Only fires when Phase 1 finds fewer than 5 skills.
         Catches novel/non-standard skill names.
"""
import json
import re
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def _load_canonical() -> dict:
    """Load canonical.json once at startup."""
    return json.loads(Path("data/skills_canonical.json").read_text())


@lru_cache(maxsize=1)
def _build_alias_map() -> dict[str, str]:
    """{ lowercased_alias: canonical_name }"""
    data = _load_canonical()
    m: dict[str, str] = {}
    for canonical, aliases in data.items():
        m[canonical.lower()] = canonical
        for alias in aliases:
            m[alias.lower()] = canonical
    return m


@lru_cache(maxsize=1)
def _get_canonical_names() -> list[str]:
    return list(_load_canonical().keys())


@lru_cache(maxsize=1)
def _get_zero_shot():
    from transformers import pipeline

    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=-1,
    )


def extract_skills(text: str) -> list[str]:
    """
    Returns deduplicated list of canonical skill names found in text.

    Phase 1: alias map keyword scan (always runs)
    Phase 2: zero-shot for novel tech tokens (only when Phase 1 < 5 results)
    """
    alias_map  = _build_alias_map()
    text_lower = text.lower()

    found: list[str] = []
    seen:  set[str]  = set()

    # Phase 1: keyword scan
    for alias, canonical in alias_map.items():
        # word-boundary check to avoid "go" matching "golang"
        if re.search(r"\b" + re.escape(alias) + r"\b", text_lower):
            if canonical not in seen:
                found.append(canonical)
                seen.add(canonical)

    if len(found) >= 5:
        return found

    # Phase 2: zero-shot on capitalized tokens not in taxonomy
    candidate_tokens = list(set(
        re.findall(r"\b[A-Z][a-zA-Z0-9+#.]{1,20}\b", text)
    ))
    unknown_tokens = [t for t in candidate_tokens if t.lower() not in alias_map][:15]

    if not unknown_tokens:
        return found

    canonical_labels = _get_canonical_names()[:50]
    classifier = _get_zero_shot()

    for token in unknown_tokens[:10]:
        try:
            result    = classifier(
                f"This person has experience with {token}",
                candidate_labels=canonical_labels,
                multi_label=False,
            )
            top_label = result["labels"][0]
            top_score = result["scores"][0]
            if top_score > 0.75 and top_label not in seen:
                found.append(top_label)
                seen.add(top_label)
        except Exception:
            continue

    return found
