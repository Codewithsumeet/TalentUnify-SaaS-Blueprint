"""
database.py — Dual-engine database module.

FastAPI (async): uses AsyncSession via postgresql+asyncpg:// URL.
Celery tasks (sync): uses standard Session via postgresql:// URL (asyncpg stripped).

NEVER import get_db() inside Celery tasks — use get_db_session() instead.
NEVER import get_db_session() inside async FastAPI routes — use get_db() instead.
"""
from contextlib import asynccontextmanager, contextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy import create_engine
from config import get_settings

settings = get_settings()


def get_async_db_url(db_url: str) -> str:
    """
    Ensures async SQLAlchemy URL for FastAPI runtime.
    postgresql://... -> postgresql+asyncpg://...
    sqlite:///... -> sqlite+aiosqlite:///...
    """
    if db_url.startswith("postgresql://"):
        return db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if db_url.startswith("sqlite:///"):
        return db_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    return db_url


def get_sync_db_url(async_url: str) -> str:
    """
    Converts async URL to psycopg (v3) URL for sync Celery tasks.
    postgresql+asyncpg://... → postgresql+psycopg://...
    postgresql://... → postgresql+psycopg://...
    """
    if async_url.startswith("postgresql+asyncpg://"):
        return async_url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    if async_url.startswith("postgresql://"):
        return async_url.replace("postgresql://", "postgresql+psycopg://", 1)
    if async_url.startswith("sqlite+aiosqlite:///"):
        return async_url.replace("sqlite+aiosqlite:///", "sqlite:///", 1)
    return async_url


# ── Async engine (FastAPI) ────────────────────────────────────────────────────
async_engine = create_async_engine(
    get_async_db_url(settings.database_url),
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_db():
    """Async context manager for FastAPI route handlers."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ── Sync engine (Celery) ──────────────────────────────────────────────────────
_sync_engine = None

def _get_sync_engine():
    global _sync_engine
    if _sync_engine is None:
        sync_url = get_sync_db_url(settings.database_url)
        _sync_engine = create_engine(
            sync_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    return _sync_engine


@contextmanager
def get_db_session():
    """
    Sync context manager for use inside Celery tasks and background functions.
    DO NOT use inside async FastAPI route handlers.
    """
    engine = _get_sync_engine()
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


@contextmanager
def get_db_context():
    """
    Sync context manager for Celery/background jobs.
    Use this in sync contexts; use get_db() in async FastAPI routes.
    """
    with get_db_session() as db:
        yield db
