"""
Tier 2A primary: contact entity extraction.
Uses spaCy en_core_web_sm + regex. Fast (5ms). Always runs.
"""
import re
from functools import lru_cache
import spacy

_EMAIL_RE    = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_PHONE_RE    = re.compile(r"(\+?[\d\s\-().]{8,17})")
_LINKEDIN_RE = re.compile(r"https?://(?:www\.)?linkedin\.com/in/[\w\-]+/?")
_GITHUB_RE   = re.compile(r"https?://(?:www\.)?github\.com/[\w\-]+/?")


@lru_cache(maxsize=1)
def _get_nlp():
    """Lazy-load spaCy model. Cached for process lifetime."""
    return spacy.load("en_core_web_sm")


def extract_with_spacy_regex(text: str) -> dict:
    """
    Primary contact extraction.
    Returns dict with all contact fields. Missing fields are None.
    """
    nlp = _get_nlp()
    doc = nlp(text[:2000])  # cap for speed

    name = next(
        (ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"),
        None,
    )
    location = next(
        (ent.text.strip() for ent in doc.ents if ent.label_ in ("GPE", "LOC")),
        None,
    )

    email    = (m := _EMAIL_RE.search(text))    and m.group(0)
    phone    = (m := _PHONE_RE.search(text))    and m.group(0).strip()
    linkedin = (m := _LINKEDIN_RE.search(text)) and m.group(0)
    github   = (m := _GITHUB_RE.search(text))   and m.group(0)

    return {
        "name":         name      or None,
        "location":     location  or None,
        "email":        email     or None,
        "phone":        phone     or None,
        "linkedin_url": linkedin  or None,
        "github_url":   github    or None,
    }
