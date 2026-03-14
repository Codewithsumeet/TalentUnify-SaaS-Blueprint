"""
Tier 2A fallback NER: yashpwr/resume-ner-bert-v2
25 entity types (NAME, COMPANY, DESIGNATION, COLLEGE, SKILLS, etc.), F1 ~90.9%.
~400 MB model. Lazy-loaded, process-level cache.

ONLY fires when spaCy returns None for name, current_company, or current_role.
"""
import re
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_ner_pipeline():
    from transformers import pipeline

    return pipeline(
        "token-classification",
        model="yashpwr/resume-ner-bert-v2",
        aggregation_strategy="simple",
        device=-1,  # CPU
    )


_ENTITY_MAP = {
    "NAME":                "name",
    "EMAIL ADDRESS":       "email",
    "SKILLS":              "skills_raw",
    "COMPANIES WORKED AT": "current_company",
    "COLLEGE NAME":        "education_institution",
    "GRADUATION YEAR":     "education_year",
    "YEARS OF EXPERIENCE": "experience_years_raw",
    "DESIGNATION":         "current_role",
    "LOCATION":            "location",
}


def extract_with_bert_ner(text: str) -> dict:
    """
    Run BERT NER on up to 1024 characters of resume text.
    Returns partial dict — only detected entity types included.
    """
    ner      = _get_ner_pipeline()
    entities = ner(text[:1024])  # BERT token limit guard

    result:       dict = {}
    skills_found: list = []

    for ent in entities:
        label      = ent["entity_group"].upper()
        value      = ent["word"].strip()
        mapped_key = _ENTITY_MAP.get(label)

        if mapped_key == "skills_raw":
            skills_found.append(value)
        elif mapped_key and mapped_key not in result:
            result[mapped_key] = value

    if skills_found:
        result["skills_raw"] = skills_found

    # Parse experience_years_raw → float
    raw_exp = result.pop("experience_years_raw", None)
    if raw_exp:
        nums = re.findall(r"\d+\.?\d*", str(raw_exp))
        if nums:
            result["experience_years"] = float(nums[0])

    return result


def extract_contact_entities_with_fallback(markdown_text: str) -> dict:
    """
    Tier 2A main entry point.

    Step 1: spaCy + regex (always, fast)
    Step 2: BERT NER (only if critical fields are missing)
    """
    from .contact_ner import extract_with_spacy_regex

    base = extract_with_spacy_regex(markdown_text)

    missing_critical = [
        f for f in ["name", "current_company", "current_role"]
        if not base.get(f)
    ]

    if missing_critical:
        bert_result = extract_with_bert_ner(markdown_text[:1500])
        for key in missing_critical:
            if bert_result.get(key):
                base[key] = bert_result[key]
        # Additive: merge BERT-detected skills regardless
        if bert_result.get("skills_raw"):
            base.setdefault("skills_bert", []).extend(bert_result["skills_raw"])

    return base
