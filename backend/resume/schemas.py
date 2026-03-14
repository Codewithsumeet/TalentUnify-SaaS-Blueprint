from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

ResumeTaskState = Literal["queued", "processing", "parsed", "failed"]


class ResumeUploadResponse(BaseModel):
    task_id: str
    status: ResumeTaskState


class ResumeTaskResult(BaseModel):
    candidate_id: UUID
    resume_id: UUID
    status: str
    extracted_preview: str | None = None


class ResumeStatusResponse(BaseModel):
    task_id: str
    status: ResumeTaskState
    result: ResumeTaskResult | None = None
    error: str | None = None


class ResumeResponse(BaseModel):
    id: UUID
    candidate_id: UUID
    file_name: str
    file_type: str
    parse_status: str
    created_at: datetime
    parsed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
