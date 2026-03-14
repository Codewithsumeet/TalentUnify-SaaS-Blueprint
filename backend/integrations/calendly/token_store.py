from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from models.integration_token import IntegrationToken

settings = get_settings()


async def get_service_token(db: AsyncSession, service: str = "calendly") -> Optional[IntegrationToken]:
    """Retrieve stored OAuth token for a service."""
    result = await db.execute(
        sa.select(IntegrationToken).where(IntegrationToken.service == service).limit(1)
    )
    return result.scalar_one_or_none()


async def get_valid_token(db: Optional[AsyncSession] = None) -> Optional[str]:
    """
    Retrieves a valid access token.
    Priority:
    1. Stored OAuth token (if DB provided)
    2. Global Personal Access Token (PAT) from configuration
    """
    if db:
        stored = await get_service_token(db, service="calendly")
        if stored and stored.access_token:
            # TODO: Add refresh logic if expires_at is in the past
            return stored.access_token

    return getattr(settings, "calendly_personal_access_token", None)


async def save_tokens(
    tokens: dict,
    db: AsyncSession,
    service: str = "calendly",
) -> IntegrationToken:
    """Store or update OAuth tokens."""
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in", 0)
    
    expires_at = None
    if expires_in:
        # Simplistic expiry calculation
        from datetime import timezone, timedelta
        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=expires_in)).replace(tzinfo=None)

    return await upsert_service_token(
        db,
        service=service,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )


async def upsert_service_token(
    db: AsyncSession,
    service: str,
    access_token: str,
    refresh_token: Optional[str] = None,
    expires_at: Optional[datetime] = None,
) -> IntegrationToken:
    existing = await get_service_token(db, service=service)
    if existing:
        existing.access_token = access_token
        existing.refresh_token = refresh_token
        existing.expires_at = expires_at
        await db.flush()
        return existing

    token = IntegrationToken(
        service=service,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )
    db.add(token)
    await db.flush()
    return token
