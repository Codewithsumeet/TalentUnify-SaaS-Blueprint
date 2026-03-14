import uuid
from datetime import datetime, timedelta, timezone

import httpx

from config import get_settings

settings = get_settings()

CALENDLY_API_BASE = "https://api.calendly.com"

FALLBACK_EVENT_TYPES = [
    {
        "uri": "https://api.calendly.com/event_types/demo-screening-30m",
        "name": "Screening Call (30m)",
        "duration": 30,
        "minNoticeHours": 4,
    },
    {
        "uri": "https://api.calendly.com/event_types/demo-technical-60m",
        "name": "Technical Interview (60m)",
        "duration": 60,
        "minNoticeHours": 24,
    },
]


def _mock_mode_enabled() -> bool:
    explicit = (getattr(settings, "calendly_mock_mode", "") or "").strip().lower()
    if explicit in {"1", "true", "yes", "on"}:
        return True
    return not bool(getattr(settings, "calendly_personal_access_token", ""))


def _auth_token(access_token: str | None) -> str:
    return access_token or getattr(settings, "calendly_personal_access_token", "") or ""


async def list_event_types(access_token: str | None = None) -> list[dict]:
    token = _auth_token(access_token)
    if _mock_mode_enabled() or not token:
        return FALLBACK_EVENT_TYPES

    headers = {"Authorization": f"Bearer {token}"}
    params = {"count": 20}
    organization_uri = getattr(settings, "calendly_organization_uri", "")
    user_uri = getattr(settings, "calendly_user_uri", "")
    if organization_uri:
        params["organization"] = organization_uri
    if user_uri:
        params["user"] = user_uri

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{CALENDLY_API_BASE}/event_types", headers=headers, params=params)
            response.raise_for_status()
            payload = response.json()
    except Exception:
        return FALLBACK_EVENT_TYPES

    collection = payload.get("collection", [])
    event_types: list[dict] = []
    for item in collection:
        event_types.append(
            {
                "uri": item.get("uri"),
                "name": item.get("name"),
                "duration": item.get("duration", 30),
                "minNoticeHours": int(item.get("minimum_notice", 0) or 0) // 3600,
            }
        )
    return event_types or FALLBACK_EVENT_TYPES


async def create_scheduling_link(
    event_type_uri: str,
    access_token: str | None = None,
    prefill: dict | None = None,
) -> dict:
    token = _auth_token(access_token)
    if _mock_mode_enabled() or not token:
        link_uuid = str(uuid.uuid4())
        return {
            "resource": {
                "booking_url": f"https://calendly.com/mock/{link_uuid}",
                "scheduling_link": f"https://calendly.com/mock/{link_uuid}",
                "scheduling_link_uuid": link_uuid,
                "event_type": event_type_uri,
                "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            }
        }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "max_event_count": 1,
        "owner": event_type_uri,
        "owner_type": "EventType",
    }
    if prefill:
        payload["invitees"] = [prefill]

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{CALENDLY_API_BASE}/scheduling_links",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
    except Exception:
        link_uuid = str(uuid.uuid4())
        return {
            "resource": {
                "booking_url": f"https://calendly.com/mock/{link_uuid}",
                "scheduling_link": f"https://calendly.com/mock/{link_uuid}",
                "scheduling_link_uuid": link_uuid,
                "event_type": event_type_uri,
                "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            }
        }

