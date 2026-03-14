from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from models.integration_token import IntegrationToken


async def get_service_token(db: AsyncSession, service: str = "calendly") -> IntegrationToken | None:
    result = await db.execute(
        sa.select(IntegrationToken).where(IntegrationToken.service == service).limit(1)
    )
    return result.scalar_one_or_none()


async def upsert_service_token(
    db: AsyncSession,
    service: str,
    access_token: str,
    refresh_token: str | None = None,
    expires_at: datetime | None = None,
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

