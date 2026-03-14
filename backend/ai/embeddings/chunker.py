"""
Section-based chunking for long resumes.
Resumes > 4000 chars are split by section, each section embedded separately,
then averaged into a single vector. This gives better semantic precision
than embedding the entire document as one blob.

Strategy inspired by ResumAI LangFlow project.
"""
import numpy as np

SECTION_HEADERS = [
    "experience", "work experience", "employment history", "professional experience",
    "education", "academic background", "educational qualifications",
    "skills", "technical skills", "core competencies", "key skills",
    "projects", "personal projects", "side projects",
    "certifications", "licenses", "achievements", "awards",
    "summary", "objective", "professional summary", "profile", "about me",
    "publications", "research", "patents",
]


def chunk_resume_for_embedding(markdown: str) -> dict[str, str]:
    """
    Splits resume markdown into named sections.
    Returns: { section_name: section_text }
    Only returns sections with non-trivial content (> 30 chars).
    """
    lines    = markdown.split("\n")
    sections: dict[str, list[str]] = {"header": []}
    current  = "header"

    for line in lines:
        stripped = line.strip()
        cleaned  = stripped.lower().strip("# -*_:•")
        matched  = next(
            (h for h in SECTION_HEADERS if h in cleaned and len(cleaned) < 60),
            None,
        )
        is_header = (
            stripped.startswith("#") or
            stripped.startswith("**") or
            stripped.isupper() and len(stripped) > 3
        )
        if matched and is_header:
            current = matched
            sections[current] = []
        else:
            sections.setdefault(current, []).append(line)

    return {
        k: "\n".join(v).strip()
        for k, v in sections.items()
        if len("\n".join(v).strip()) > 30
    }


async def get_aggregate_embedding(markdown: str) -> list[float]:
    """
    For resumes > 4000 chars: chunk → embed each section → L2-normalised average.
    For shorter resumes: single full-text embedding.

    Always routes to the correct Pinecone index via client.get_active_index_name().
    """
    from .client import get_embedding

    if len(markdown) < 4000:
        return await get_embedding(markdown)

    chunks     = chunk_resume_for_embedding(markdown)
    embeddings = []

    for section, text in chunks.items():
        if len(text.strip()) < 50:
            continue
        try:
            emb = await get_embedding(text)
            embeddings.append(emb)
        except Exception:
            continue

    if not embeddings:
        return await get_embedding(markdown[:4000])

    arr  = np.array(embeddings, dtype=float)
    avg  = np.mean(arr, axis=0)
    norm = np.linalg.norm(avg)
    return (avg / norm if norm > 1e-9 else avg).tolist()
