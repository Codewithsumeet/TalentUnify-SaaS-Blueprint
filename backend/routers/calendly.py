import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import get_db
from integrations.calendly.service import create_scheduling_link, list_event_types
from integrations.calendly.token_store import get_service_token
from models.candidate import Candidate
from models.scheduled_interview import ScheduledInterview

router = APIRouter(prefix="/api/v1", tags=["calendly"])

ALLOWED_PIPELINE_STAGES = {"screening", "interview", "offer"}


class ScheduleRequest(BaseModel):
    event_type_uri: str
    prefill: dict | None = None


@router.get("/integration/calendly/event-types")
async def calendly_event_types():
    async with get_db() as db:
        token = await get_service_token(db, service="calendly")
        token_value = token.access_token if token else None
    return await list_event_types(token_value)


@router.post("/candidates/{candidate_id}/schedule")
async def schedule_candidate_interview(candidate_id: str, payload: ScheduleRequest):
    try:
        candidate_uuid = uuid.UUID(candidate_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid candidate id") from exc

    async with get_db() as db:
        candidate_result = await db.execute(sa.select(Candidate).where(Candidate.id == candidate_uuid))
        candidate = candidate_result.scalar_one_or_none()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        if candidate.status != "active":
            raise HTTPException(status_code=400, detail="Candidate is not active")

        stage = (candidate.pipeline_stage or "applied").lower()
        if stage not in ALLOWED_PIPELINE_STAGES:
            raise HTTPException(
                status_code=400,
                detail="Interview scheduling allowed only in screening/interview/offer stage",
            )

        token = await get_service_token(db, service="calendly")
        calendly_response = await create_scheduling_link(
            event_type_uri=payload.event_type_uri,
            access_token=token.access_token if token else None,
            prefill=payload.prefill or {},
        )

        resource = calendly_response.get("resource", {})
        scheduling_url = resource.get("booking_url") or resource.get("scheduling_link")
        if not scheduling_url:
            raise HTTPException(status_code=502, detail="Calendly did not return a scheduling URL")

        interview = ScheduledInterview(
            candidate_id=candidate.id,
            event_type_uri=payload.event_type_uri,
            calendly_link=scheduling_url,
            scheduling_link_uuid=resource.get("scheduling_link_uuid"),
            calendly_event_uri=resource.get("event_type"),
            status="link_created",
            scheduled_at=None,
            invitee_name=(payload.prefill or {}).get("name"),
            invitee_email=(payload.prefill or {}).get("email"),
            created_at=datetime.now(timezone.utc),
        )
        db.add(interview)
        await db.flush()
        await db.refresh(interview)

    return {
        "interview_id": str(interview.id),
        "scheduling_url": interview.calendly_link,
        "scheduling_link_uuid": interview.scheduling_link_uuid,
        "event_type_uri": interview.event_type_uri,
    }

