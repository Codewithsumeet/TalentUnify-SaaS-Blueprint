"""
LinkedIn public profile ingestor (dummy scraper).

Accepts a LinkedIn URL, fetches page content, strips HTML, and queues the
result through the existing resume parsing pipeline for enrichment.
"""

from __future__ import annotations

import re
import uuid

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

router = APIRouter(prefix="/api/v1/integrations/linkedin")


class LinkedInFetchRequest(BaseModel):
    url: HttpUrl


def _extract_text_from_html(html: str) -> str:
    no_script = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    plain = re.sub(r"<[^>]+>", " ", no_script)
    compact = re.sub(r"\s+", " ", plain).strip()
    return compact[:80_000]


@router.post("/fetch")
async def fetch_linkedin_profile(payload: LinkedInFetchRequest):
    target_url = str(payload.url).strip()
    if "linkedin.com" not in target_url.lower():
        raise HTTPException(status_code=400, detail="Only linkedin.com URLs are supported.")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        async with httpx.AsyncClient(timeout=25.0, follow_redirects=True, headers=headers) as client:
            response = await client.get(target_url)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch LinkedIn URL: {exc}") from exc

    if response.status_code >= 400:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to fetch profile content (status {response.status_code}).",
        )

    extracted_text = _extract_text_from_html(response.text)
    if len(extracted_text) < 40:
        raise HTTPException(status_code=422, detail="Profile content was too short to parse.")

    markdown = (
        "# LinkedIn Public Profile\n\n"
        f"Source URL: {target_url}\n\n"
        "## Extracted Content\n"
        f"{extracted_text}\n"
    )

    from tasks.resume_tasks import parse_resume_task

    task_id = str(uuid.uuid4())
    parse_resume_task.apply_async(
        kwargs={
            "file_bytes": markdown.encode("utf-8"),
            "mime_type": "text/markdown",
            "source": "linkedin",
            "filename": "linkedin_profile.md",
            "metadata": {"linkedin_url": target_url, "source_system": "linkedin_dummy_scraper"},
        },
        task_id=task_id,
    )
    return {
        "status": "queued",
        "task_id": task_id,
        "source": "linkedin",
        "url": target_url,
        "preview_chars": len(extracted_text),
    }
