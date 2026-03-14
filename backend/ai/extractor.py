"""
Tier 1: Document → Structured Markdown.

Three-tier fallback chain:
  PRIMARY:            LlamaParse (layout-aware, OCR, tables, Devanagari)
  SECONDARY FALLBACK: csccorner/Agentic-Resume-Parser HF Space API
  EMERGENCY FALLBACK: pypdf + python-docx (raw text, no layout)

Returns: { markdown: str, quality: "high"|"medium"|"low", parser_used: str }
"""
import os
import base64
import tempfile
from io import BytesIO
from pathlib import Path

import httpx
import pypdf
import docx as python_docx
try:
    from llama_parse import LlamaParse
except Exception:  # pragma: no cover - optional dependency
    LlamaParse = None

from config import get_settings

settings = get_settings()

# Lazy-init LlamaParse to avoid import error if API key not set during testing
_llamaparse_instance = None

def _get_llamaparse() -> LlamaParse | None:
    global _llamaparse_instance
    if LlamaParse is None or not settings.llama_cloud_api_key:
        return None
    if _llamaparse_instance is None:
        _llamaparse_instance = LlamaParse(
            api_key=settings.llama_cloud_api_key,
            result_type="markdown",
            verbose=False,
        )
    return _llamaparse_instance


async def extract_to_markdown(file_bytes: bytes, mime_type: str) -> dict:
    """
    Main Tier 1 entry point.
    Returns: { markdown: str, quality: "high"|"medium"|"low", parser_used: str }
    """

    # ── PRIMARY: LlamaParse ───────────────────────────────────────────────────
    try:
        suffix = ".pdf" if "pdf" in mime_type else ".docx"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        try:
            parser    = _get_llamaparse()
            if parser is None:
                raise RuntimeError("LlamaParse is unavailable")
            documents = await parser.aload_data(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        if documents and documents[0].text.strip():
            return {
                "markdown":    documents[0].text,
                "quality":     "high",
                "parser_used": "llamaparse",
            }
    except Exception:
        pass  # fall through to secondary

    # ── SECONDARY FALLBACK: Agentic HF Space ──────────────────────────────────
    try:
        hf_markdown = await _agentic_hf_fallback(file_bytes)
        if hf_markdown and len(hf_markdown.strip()) > 100:
            return {
                "markdown":    hf_markdown,
                "quality":     "medium",
                "parser_used": "agentic_hf_space",
            }
    except Exception:
        pass

    # ── EMERGENCY FALLBACK: pypdf / python-docx ───────────────────────────────
    raw_text = _extract_raw_text(file_bytes, mime_type)
    return {
        "markdown":    raw_text or "(parse_failed: no text extracted)",
        "quality":     "low",
        "parser_used": "pypdf_fallback",
    }


async def _agentic_hf_fallback(file_bytes: bytes) -> str:
    """
    Calls csccorner/Agentic-Resume-Parser HF Space public inference API.
    Free to call — public HF Space.
    """
    encoded = base64.b64encode(file_bytes).decode()
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp   = await client.post(
            "https://csccorner-agentic-resume-parser.hf.space/api/predict",
            json={"data": [encoded]},
        )
        result = resp.json()
        return result.get("data", [{}])[0].get("markdown", "")


def _extract_raw_text(file_bytes: bytes, mime_type: str) -> str:
    """Emergency raw text extraction. Also called directly on LlamaParse timeout."""
    try:
        if "pdf" in mime_type:
            reader = pypdf.PdfReader(BytesIO(file_bytes))
            return "\n".join(
                page.extract_text() or "" for page in reader.pages
            )
        else:
            doc = python_docx.Document(BytesIO(file_bytes))
            return "\n".join(para.text for para in doc.paragraphs)
    except Exception:
        return ""
