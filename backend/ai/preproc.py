"""
Tier 0: Pre-processing.
Pure Python stdlib — zero external dependencies.
Runs synchronously as the very first step before any AI call.
"""
import re
import mimetypes
from pathlib import Path

_EMAIL_RE    = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_PHONE_RE    = re.compile(r"(\+?[\d\s\-().]{8,17})")
_LINKEDIN_RE = re.compile(r"https?://(?:www\.)?linkedin\.com/in/[\w\-]+/?")
_GITHUB_RE   = re.compile(r"https?://(?:www\.)?github\.com/[\w\-]+/?")

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def preprocess_file(file_bytes: bytes, mime_type: str, filename: str) -> dict:
    """
    Tier 0 validation and basic extraction.
    Returns: { ok: bool, error: str|None, mime_type: str, size_bytes: int }
    """
    size = len(file_bytes)

    if size > MAX_FILE_SIZE_BYTES:
        return {"ok": False, "error": f"File too large: {size} bytes. Max 10 MB."}

    # Normalise mime type — some clients send wrong content-type
    if mime_type not in ALLOWED_MIME_TYPES:
        guessed, _ = mimetypes.guess_type(filename)
        if guessed in ALLOWED_MIME_TYPES:
            mime_type = guessed
        else:
            return {"ok": False, "error": f"Unsupported file type: {mime_type}"}

    return {
        "ok":         True,
        "error":      None,
        "mime_type":  mime_type,
        "size_bytes": size,
    }


def quick_extract_contacts(text: str) -> dict:
    """
    Regex-only contact extraction from raw text.
    Runs BEFORE spaCy — provides seeding hints to later NER stages.
    """
    email    = (m := _EMAIL_RE.search(text))    and m.group(0)
    phone    = (m := _PHONE_RE.search(text))    and m.group(0).strip()
    linkedin = (m := _LINKEDIN_RE.search(text)) and m.group(0)
    github   = (m := _GITHUB_RE.search(text))   and m.group(0)
    return {
        "email":        email   or None,
        "phone":        phone   or None,
        "linkedin_url": linkedin or None,
        "github_url":   github  or None,
    }
