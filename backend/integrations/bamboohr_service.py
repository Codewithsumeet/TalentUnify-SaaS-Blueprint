from __future__ import annotations

import logging

import httpx

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _split_name(full_name: str) -> tuple[str, str]:
    clean = (full_name or "").strip()
    if not clean:
        return "Candidate", "Imported"
    parts = clean.split()
    if len(parts) == 1:
        return parts[0], "Imported"
    return parts[0], " ".join(parts[1:])


async def push_candidate_to_bamboohr(candidate_payload: dict) -> dict:
    """
    Push a hired candidate profile to BambooHR.
    Uses API key basic auth (API key as username, password placeholder "x").
    """
    if not settings.bamboo_api_key or not settings.bamboo_domain:
        return {"status": "skipped", "reason": "bamboo_not_configured"}

    email = str(candidate_payload.get("email") or "").strip()
    if not email:
        return {"status": "skipped", "reason": "candidate_email_missing"}

    first_name, last_name = _split_name(str(candidate_payload.get("name") or ""))
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "workEmail": email,
        "jobTitle": candidate_payload.get("current_role") or "New Hire",
        "location": candidate_payload.get("location") or "Unknown",
    }

    endpoint = f"https://api.bamboohr.com/api/gateway.php/{settings.bamboo_domain}/v1/employees/"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            endpoint,
            json=payload,
            auth=(settings.bamboo_api_key, "x"),
            headers=headers,
        )

    if response.status_code >= 400:
        logger.error(
            "BambooHR sync failed for candidate=%s status=%s body=%s",
            candidate_payload.get("id"),
            response.status_code,
            response.text[:300],
        )
        return {"status": "failed", "code": response.status_code}

    return {
        "status": "synced",
        "candidate_id": candidate_payload.get("id"),
        "response_code": response.status_code,
    }
