"""
Calendly Router - Unified Implementation
OAuth flow, scheduling management, and secure webhook processing.
"""
from __future__ import annotations

import hashlib
import hmac
import logging
from datetime import datetime, timezone
from uuid import UUID
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import httpx
import sqlalchemy as sa
from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from config import get_settings
from database import get_db
from integrations.calendly.service import CalendlyService
from integrations.calendly.token_store import get_valid_token, save_tokens
from models.candidate import Candidate
from models.scheduled_interview import ScheduledInterview

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/integration/calendly", tags=["calendly"])
settings = get_settings()

CALENDLY_AUTH_URL = "https://auth.calendly.com/oauth/authorize"
CALENDLY_TOKEN_URL = "https://auth.calendly.com/oauth/token"


def _resolve_frontend_return_target(return_to: str | None = None) -> str:
    default_origin = getattr(settings, "frontend_url", "http://localhost:3000").rstrip("/")
    default_target = f"{default_origin}/integrations"
    if not return_to:
        return default_target

    parsed = urlparse(return_to)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return default_target

    origin = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
    allowed_origins = {
        default_origin,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    }
    if origin not in allowed_origins:
        return default_target

    path = parsed.path or "/integrations"
    return f"{origin}{path}"


def _frontend_integrations_url(status: str, return_to: str | None = None) -> str:
    target = _resolve_frontend_return_target(return_to)
    parsed = urlparse(target)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["calendly"] = status
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            urlencode(query),
            parsed.fragment,
        )
    )


# ── OAuth Flow ───────────────────────────────────────────────────────────────

@router.get("/connect", summary="Start Calendly OAuth flow")
async def calendly_connect(return_to: str | None = None):
    """Redirect recruiter to Calendly's OAuth consent page."""
    # Ensure settings have OAuth credentials
    client_id = getattr(settings, "calendly_client_id", None)
    redirect_uri = getattr(settings, "calendly_redirect_uri", None)
    
    if not client_id or not redirect_uri:
        mock_mode = bool(getattr(settings, "calendly_mock_mode", False))
        if mock_mode:
            return RedirectResponse(_frontend_integrations_url("mock-connected", return_to))
        return RedirectResponse(_frontend_integrations_url("not-configured", return_to))
        
    params = {
        "client_id":     client_id,
        "response_type": "code",
        "redirect_uri":  redirect_uri,
        "state": return_to or "",
    }
    return RedirectResponse(f"{CALENDLY_AUTH_URL}?{urlencode(params)}")


@router.get("/callback", summary="Calendly OAuth callback")
async def calendly_callback(code: str, state: str | None = None):
    """Exchange auth code for tokens; persist in DB."""
    client_id = getattr(settings, "calendly_client_id", None)
    client_secret = getattr(settings, "calendly_client_secret", None)
    redirect_uri = getattr(settings, "calendly_redirect_uri", None)

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                CALENDLY_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
            )
    except Exception:
        logger.exception("Calendly callback failed during token exchange request")
        return RedirectResponse(_frontend_integrations_url("token-error", state))

    if resp.status_code != 200:
        logger.error(f"Calendly callback failed: {resp.text}")
        return RedirectResponse(_frontend_integrations_url("token-error", state))

    try:
        tokens = resp.json()
    except ValueError:
        logger.error("Calendly callback returned non-JSON token payload")
        return RedirectResponse(_frontend_integrations_url("token-error", state))

    if not tokens.get("access_token"):
        logger.error("Calendly callback payload missing access_token")
        return RedirectResponse(_frontend_integrations_url("token-error", state))

    try:
        async with get_db() as db:
            await save_tokens(tokens, db)
    except Exception:
        logger.exception("Calendly callback failed while saving tokens")
        return RedirectResponse(_frontend_integrations_url("callback-error", state))

    return RedirectResponse(_frontend_integrations_url("connected", state))


# ── Management Endpoints ─────────────────────────────────────────────────────

@router.get("/event-types", summary="List Calendly event types")
async def list_calendly_event_types():
    """Fetch event types using stored OAuth token or global PAT."""
    async with get_db() as db:
        token = await get_valid_token(db)
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Calendly not connected. Please visit /integration/calendly/connect"
            )

        try:
            svc = CalendlyService(token)
            # Use me/org discovery
            user_data = await svc.get_user()
            user_uri = user_data["resource"]["uri"]
            event_types = await svc.get_event_types(user_uri)
            return {"event_types": event_types.get("collection", [])}
        except Exception:
            logger.exception("Failed to fetch Calendly event types")
            raise HTTPException(status_code=502, detail="Failed to fetch from Calendly")


class ScheduleRequest(BaseModel):
    event_type_uri: str
    prefill: dict | None = None


@router.post("/candidates/{candidate_id}/schedule", summary="Generate a booking link for a candidate")
async def schedule_candidate_interview(
    candidate_id: UUID,
    body: ScheduleRequest,
):
    """
    Creates a single-use Calendly scheduling link and records it in ScheduledInterview.
    """
    async with get_db() as db:
        # 1. Fetch Candidate
        candidate_result = await db.execute(sa.select(Candidate).where(Candidate.id == candidate_id))
        candidate = candidate_result.scalar_one_or_none()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        # 2. Get Valid Token
        token = await get_valid_token(db)
        if not token:
            raise HTTPException(status_code=401, detail="Calendly not connected")

        # 3. Create Link
        svc = CalendlyService(token)
        try:
            link_data = await svc.create_scheduling_link(
                event_type_uri=body.event_type_uri,
                max_event_count=1,
                prefill=body.prefill
            )
        except Exception:
            logger.exception("Calendly link creation failed")
            raise HTTPException(status_code=502, detail="Failed to create Calendly link")

        resource = link_data.get("resource", {})
        booking_url = resource.get("booking_url") or resource.get("scheduling_link")
        if not booking_url:
            raise HTTPException(status_code=502, detail="Calendly did not return booking url")
        
        # 4. Record Interview
        interview = ScheduledInterview(
            candidate_id=candidate.id,
            event_type_uri=body.event_type_uri,
            calendly_link=booking_url,
            scheduling_link_uuid=resource.get("scheduling_link_uuid"),
            status="link_created",
            created_at=datetime.now(timezone.utc),
            invitee_email=body.prefill.get("email") if body.prefill else candidate.email,
            invitee_name=body.prefill.get("name") if body.prefill else candidate.name,
        )
        db.add(interview)
        await db.flush()
        await db.refresh(interview)

    return {
        "candidate_id": str(candidate.id),
        "booking_url":  booking_url,
        "interview_id": str(interview.id)
    }


# ── Webhook Handler ──────────────────────────────────────────────────────────

@router.post("/webhook", summary="Receive Calendly webhook transitions")
async def calendly_webhook(
    request: Request,
    calendly_webhook_signature: str | None = Header(None, alias="Calendly-Webhook-Signature"),
):
    """
    Securely process Calendly webhooks.
    Transitions candidate to 'Interview' stage on 'invitee.created'.
    """
    raw_body = await request.body()
    webhook_secret = getattr(settings, "calendly_webhook_secret", None)

    # Validate signature if configured
    if webhook_secret and calendly_webhook_signature:
        expected = hmac.new(
            webhook_secret.encode(),
            raw_body,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, calendly_webhook_signature):
            logger.warning("Invalid Calendly webhook signature received")
            raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    event_type = payload.get("event")

    if event_type == "invitee.created":
        invitee_payload = payload.get("payload", {})
        invitee = invitee_payload.get("invitee", {})
        email = str(invitee.get("email", "")).lower()

        if email:
            async with get_db() as db:
                # Find candidate and update stage
                result = await db.execute(sa.select(Candidate).where(Candidate.email == email))
                candidate = result.scalar_one_or_none()
                if candidate:
                    candidate.pipeline_stage = "Interview"
                    await db.flush()
                    logger.info(f"Webhook: Candidate {candidate.id} moved to Interview stage")
                    return {"updated": True, "candidate_id": str(candidate.id)}

    return {"received": True, "event": event_type}
