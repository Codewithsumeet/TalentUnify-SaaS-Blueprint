from __future__ import annotations

import logging
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.dependencies import get_current_user
from config import get_settings
from database import get_db
from integrations.calendly.token_store import get_service_token, save_tokens
from integrations.gmail.native_service import SCOPES, poll_gmail_for_resumes

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter(prefix="/api/v1/integration/gmail", tags=["gmail"])


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
    query["gmail"] = status
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


@router.get("/connect", summary="Start Gmail OAuth flow")
async def gmail_connect(return_to: str | None = None):
    client_id = getattr(settings, "gmail_client_id", "")
    client_secret = getattr(settings, "gmail_client_secret", "")
    redirect_uri = getattr(settings, "gmail_redirect_uri", "")
    if not client_id or not client_secret or not redirect_uri:
        return RedirectResponse(_frontend_integrations_url("not-configured", return_to))

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "consent",
        "state": return_to or "",
    }
    return RedirectResponse(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


@router.get("/callback", summary="Gmail OAuth callback")
async def gmail_callback(code: str, state: str | None = None):
    client_id = getattr(settings, "gmail_client_id", "")
    client_secret = getattr(settings, "gmail_client_secret", "")
    redirect_uri = getattr(settings, "gmail_redirect_uri", "")
    if not client_id or not client_secret or not redirect_uri:
        return RedirectResponse(_frontend_integrations_url("not-configured", state))

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
    except Exception:
        logger.exception("Gmail callback failed during token exchange request")
        return RedirectResponse(_frontend_integrations_url("token-error", state))

    if response.status_code != 200:
        logger.error("Gmail callback failed: status=%s body=%s", response.status_code, response.text[:300])
        return RedirectResponse(_frontend_integrations_url("token-error", state))

    try:
        tokens = response.json()
    except ValueError:
        logger.error("Gmail callback returned non-JSON token payload")
        return RedirectResponse(_frontend_integrations_url("token-error", state))

    if not tokens.get("access_token"):
        logger.error("Gmail callback payload missing access_token")
        return RedirectResponse(_frontend_integrations_url("token-error", state))

    try:
        async with get_db() as db:
            await save_tokens(tokens, db, service="gmail")
    except Exception:
        logger.exception("Gmail callback failed while saving tokens")
        return RedirectResponse(_frontend_integrations_url("callback-error", state))

    return RedirectResponse(_frontend_integrations_url("connected", state))


@router.get("/status", dependencies=[Depends(get_current_user)], summary="Get Gmail integration status")
async def gmail_status():
    async with get_db() as db:
        token = await get_service_token(db, service="gmail")

    if not token:
        return {"connected": False, "expires_at": None}

    return {
        "connected": bool(token.access_token),
        "expires_at": token.expires_at.isoformat() if token.expires_at else None,
    }


@router.post("/sync", dependencies=[Depends(get_current_user)], summary="Sync Gmail attachments now")
async def gmail_sync_now():
    client_id = getattr(settings, "gmail_client_id", "")
    client_secret = getattr(settings, "gmail_client_secret", "")
    if not client_id or not client_secret:
        raise HTTPException(status_code=400, detail="Gmail OAuth not configured")

    async with get_db() as db:
        token = await get_service_token(db, service="gmail")

    if not token:
        raise HTTPException(status_code=401, detail="Gmail not connected")

    credentials_payload = {
        "token": token.access_token,
        "refresh_token": token.refresh_token,
        "token_uri": GOOGLE_TOKEN_URL,
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": SCOPES,
    }
    try:
        task_ids = poll_gmail_for_resumes(credentials_payload)
    except Exception as exc:
        logger.exception("Gmail sync failed")
        raise HTTPException(status_code=502, detail=f"Gmail sync failed: {exc}") from exc

    return {
        "status": "queued",
        "queued": len(task_ids),
        "task_ids": task_ids,
    }
