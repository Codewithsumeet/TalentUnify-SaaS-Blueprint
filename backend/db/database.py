"""
database.py — Dual-engine isolation.

FastAPI routes  → AsyncSession  via postgresql+asyncpg://
Celery tasks    → sync Session  via postgresql://        (psycopg2)
Alembic         → sync Session  via postgresql://        (psycopg2)

NEVER mix these two contexts. Never import get_db() in Celery tasks.
Never import get_db_session() in async FastAPI routes.
"""
from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from db.base import Base
from db import models  # noqa: F401

from app.config import get_settings

settings = get_settings()


def get_async_db_url(db_url: str) -> str:
    """
    Ensure async SQLAlchemy URL for FastAPI runtime.
    """
    if db_url.startswith("postgresql://"):
        return db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if db_url.startswith("sqlite:///"):
        return db_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    return db_url


def get_sync_db_url(async_url: str) -> str:
    """
    Convert async URL → psycopg (v3) URL for sync contexts.
    postgresql+asyncpg://... → postgresql+psycopg://...
    postgresql://...         → postgresql+psycopg://...
    """
    if async_url.startswith("postgresql+asyncpg://"):
        return async_url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    if async_url.startswith("postgresql://"):
        return async_url.replace("postgresql://", "postgresql+psycopg://", 1)
    if async_url.startswith("sqlite+aiosqlite:///"):
        return async_url.replace("sqlite+aiosqlite:///", "sqlite:///", 1)
    return async_url


# ── Async engine — FastAPI only ───────────────────────────────────────────────

async_engine = create_async_engine(
    get_async_db_url(settings.database_url),
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Backward-compatible alias for modules that may still import _async_engine.
_async_engine = async_engine

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db() -> AsyncSession:
    """Async context manager for FastAPI route handlers."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_db_session():
    """Backward-compatible async dependency for existing app modules."""
    async with AsyncSessionLocal() as session:
        yield session


# ── Sync engine — Celery + Alembic only ──────────────────────────────────────

_sync_engine = None


def _get_sync_engine():
    global _sync_engine
    if _sync_engine is None:
        _sync_engine = create_engine(
            get_sync_db_url(settings.database_url),
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    return _sync_engine


@contextmanager
def get_sync_db() -> Session:
    """
    Sync context manager for Celery tasks and Alembic.
    DO NOT use inside async FastAPI route handlers.
    """
    with Session(_get_sync_engine()) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
