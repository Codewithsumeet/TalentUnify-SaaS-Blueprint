"""
FastAPI application factory.
Creates the app, adds CORS middleware, mounts all routers.
"""
from pathlib import Path
import sys
from contextlib import asynccontextmanager

backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models  # noqa: F401
from db import models as db_models  # noqa: F401
from db.base import Base as DbBase
from db.database import async_engine as db_async_engine
from app.exceptions import register_exception_handlers
from app.runtime_migrations import ensure_candidate_source_column
from api.routes import router as main_router
from api.events import router as events_router
from auth.router import router as auth_router
from integrations.gmail.n8n_bridge import router as gmail_router
from integrations.gmail.oauth_router import router as gmail_oauth_router
from integrations.hrms_mock import router as hrms_router
from integrations.linkedin_ingestor import router as linkedin_ingestor_router
from integrations.linkedin_sim import router as linkedin_router
from routers.analytics import router as analytics_router
from routers.calendly import router as calendly_router
from routers.shortlist import router as shortlist_router
from resume.router import router as resume_router
from database import async_engine, Base
from app.config import get_settings

settings = get_settings()
configured_cors_origins = settings.cors_origins_list
if configured_cors_origins == ["*"]:
    cors_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
else:
    cors_origins = configured_cors_origins
allow_credentials = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup if they don't exist."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with db_async_engine.begin() as conn:
        await conn.run_sync(DbBase.metadata.create_all)
        await conn.run_sync(ensure_candidate_source_column)
    try:
        yield
    finally:
        await async_engine.dispose()
        await db_async_engine.dispose()


app = FastAPI(
    title="TalentFlow AI",
    description="Unified AI-powered recruitment platform — Team Nexus",
    version="2.1.0",
    lifespan=lifespan,
)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = cors_origins,
    allow_credentials = allow_credentials,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

app.include_router(auth_router)
app.include_router(main_router)
app.include_router(resume_router)
app.include_router(events_router)
app.include_router(gmail_router)
app.include_router(gmail_oauth_router)
app.include_router(hrms_router)
app.include_router(linkedin_ingestor_router)
app.include_router(linkedin_router)
app.include_router(shortlist_router)
app.include_router(analytics_router)
app.include_router(calendly_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "talentflow-ai", "version": "2.1.0"}
