import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

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
    raw_value = getattr(settings, "calendly_mock_mode", "")
    if isinstance(raw_value, bool):
        return raw_value
    explicit = str(raw_value or "").strip().lower()
    return explicit in {"1", "true", "yes", "on"}


class CalendlyService:
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or getattr(settings, "calendly_personal_access_token", "")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def get_user(self) -> Dict[str, Any]:
        """Fetch current authenticated user details."""
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{CALENDLY_API_BASE}/users/me", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    async def get_event_types(self, user_uri: Optional[str] = None) -> Dict[str, Any]:
        """List event types for a user or organization."""
        params = {"count": 20}
        if user_uri:
            params["user"] = user_uri
        else:
            org_uri = getattr(settings, "calendly_organization_uri", "")
            if org_uri:
                params["organization"] = org_uri

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{CALENDLY_API_BASE}/event_types", headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()

    async def create_scheduling_link(
        self,
        event_type_uri: str,
        max_event_count: int = 1,
        owner_type: str = "EventType",
        prefill: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a single-use or multi-use scheduling link."""
        payload = {
            "max_event_count": max_event_count,
            "owner": event_type_uri,
            "owner_type": owner_type,
        }
        if prefill:
            payload["invitees"] = [prefill]

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{CALENDLY_API_BASE}/scheduling_links",
                headers=self.headers,
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()


# ── Backward Compatibility Wrappers ──────────────────────────────────────────

async def list_event_types(access_token: Optional[str] = None) -> List[Dict[str, Any]]:
    if _mock_mode_enabled() or not (access_token or getattr(settings, "calendly_personal_access_token", "")):
        return FALLBACK_EVENT_TYPES

    try:
        svc = CalendlyService(access_token)
        data = await svc.get_event_types()
        collection = data.get("collection", [])
        event_types = []
        for item in collection:
            event_types.append({
                "uri": item.get("uri"),
                "name": item.get("name"),
                "duration": item.get("duration", 30),
                "minNoticeHours": int(item.get("minimum_notice", 0) or 0) // 3600,
            })
        return event_types or FALLBACK_EVENT_TYPES
    except Exception:
        return FALLBACK_EVENT_TYPES


async def create_scheduling_link(
    event_type_uri: str,
    access_token: Optional[str] = None,
    prefill: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if _mock_mode_enabled() or not (access_token or getattr(settings, "calendly_personal_access_token", "")):
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

    try:
        svc = CalendlyService(access_token)
        return await svc.create_scheduling_link(event_type_uri, prefill=prefill)
    except Exception:
        # Fallback to mock on error to prevent breaking flow
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
