"""
Tier 2C: Job title normalization via TechWolf/JobBERT-v3.
Contrastive similarity model. ~140 MB. Lazy-loaded.

Confidence gate: only returns canonical title when similarity > 0.75.
Returns original raw title unchanged if no confident match found.
"""
import numpy as np
from functools import lru_cache


CANONICAL_TITLES = [
    "Software Engineer",        "Senior Software Engineer",    "Staff Engineer",
    "Principal Engineer",       "Engineering Manager",          "VP Engineering",
    "Frontend Engineer",        "Backend Engineer",             "Full Stack Engineer",
    "DevOps Engineer",          "Site Reliability Engineer",    "Platform Engineer",
    "Data Scientist",           "ML Engineer",                  "AI Engineer",
    "Data Engineer",            "Analytics Engineer",
    "Product Designer",         "UX Designer",                  "UI Designer",
    "Product Manager",          "Technical Product Manager",
    "QA Engineer",              "Test Engineer",                "SDET",
    "Mobile Engineer",          "iOS Engineer",                 "Android Engineer",
    "Security Engineer",        "Cloud Architect",              "Solutions Architect",
    "Tech Lead",                "CTO",                          "VP Engineering",
    "Fresher",                  "Intern",                       "Trainee",
]


@lru_cache(maxsize=1)
def _get_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("TechWolf/JobBERT-v3")


@lru_cache(maxsize=1)
def _get_canonical_embeddings():
    """Pre-compute canonical title embeddings once."""
    model = _get_model()
    return model.encode(CANONICAL_TITLES, normalize_embeddings=True)


@lru_cache(maxsize=512)
def normalize_job_title(raw_title: str) -> str:
    """
    Returns canonical title string if cosine similarity > 0.75.
    Returns raw_title unchanged if no confident match.
    """
    if not raw_title or len(raw_title.strip()) < 2:
        return raw_title

    model        = _get_model()
    raw_emb      = model.encode(raw_title, normalize_embeddings=True)
    canon_embs   = _get_canonical_embeddings()
    similarities = np.dot(canon_embs, raw_emb)

    best_idx   = int(np.argmax(similarities))
    best_score = float(similarities[best_idx])

    if best_score > 0.75:
        return CANONICAL_TITLES[best_idx]
    return raw_title
