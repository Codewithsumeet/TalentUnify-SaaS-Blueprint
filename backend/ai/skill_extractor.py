"""
Tier 2B: Two-phase skill extraction.

Phase 1: keyword alias scan against skills_canonical.json   — ~1ms, free
Phase 2: facebook/bart-large-mnli BATCHED zero-shot         — ~800ms, capped at 6 tokens
         Only fires when Phase 1 finds < 5 skills.
"""
import json
import re
from functools import lru_cache
from pathlib import Path

from transformers import pipeline as hf_pipeline


@lru_cache(maxsize=1)
def _canonical() -> dict:
    """Load skills_canonical.json once at process startup."""
    path = Path(__file__).parent.parent / "data" / "skills_canonical.json"
    return json.loads(path.read_text())


@lru_cache(maxsize=1)
def _alias_map() -> dict[str, str]:
    """{ lowercased_alias: canonical_name }"""
    data = _canonical()
    m: dict[str, str] = {}
    for canon, aliases in data.items():
        m[canon.lower()] = canon
        for alias in aliases:
            m[alias.lower()] = canon
    return m


@lru_cache(maxsize=1)
def _canonical_names() -> list[str]:
    return list(_canonical().keys())


@lru_cache(maxsize=1)
def _zero_shot():
    """Lazy-load bart-large-mnli once. Process-level cache — not re-loaded between tasks."""
    return hf_pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=-1,  # CPU
    )


def extract_skills(text: str) -> list[str]:
    """
    Returns deduplicated list of canonical skill names found in text.
    Phase 1 always runs. Phase 2 only runs when Phase 1 returns < 5 results.
    """
    alias_map  = _alias_map()
    text_lower = text.lower()
    found: list[str] = []
    seen:  set[str]  = set()

    # ── Phase 1: keyword alias scan (1ms) ────────────────────────────────────
    for alias, canon in alias_map.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", text_lower):
            if canon not in seen:
                found.append(canon)
                seen.add(canon)

    if len(found) >= 5:
        return found   # Phase 1 was sufficient — skip expensive inference

    # ── Phase 2: batched zero-shot on unknown capitalized tokens ─────────────
    # BUG FIX 6: Collect unknown tokens first, then run ONE batched call.
    # This replaces the original loop of up to 20 sequential inferences.

    candidate_tokens = list(set(re.findall(r"\b[A-Z][a-zA-Z0-9+#.]{1,20}\b", text)))
    unknown_tokens   = [t for t in candidate_tokens if t.lower() not in alias_map]

    # Hard cap: max 6 tokens submitted to zero-shot (prevents CPU DOS)
    unknown_tokens = unknown_tokens[:6]

    if not unknown_tokens:
        return found

    canon_labels = _canonical_names()[:50]
    classifier   = _zero_shot()

    try:
        # Single batched call — bart handles multi-sequence natively
        # Each token becomes one hypothesis: "This person knows {token}"
        hypotheses = [f"This person knows {tok}" for tok in unknown_tokens]
        results    = classifier(hypotheses, candidate_labels=canon_labels, multi_label=False)

        # results is a list when input is a list
        if not isinstance(results, list):
            results = [results]

        for res in results:
            top_label = res["labels"][0]
            top_score = res["scores"][0]
            # BUG FIX 6: raised threshold to 0.80 (was 0.75) — reduces false positives
            if top_score > 0.80 and top_label not in seen:
                found.append(top_label)
                seen.add(top_label)

    except Exception:
        pass  # Zero-shot failure is non-fatal — Phase 1 results still returned

    return found
