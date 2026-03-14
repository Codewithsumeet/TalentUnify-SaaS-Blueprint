from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

CandidateStatus = Literal["applied", "screened", "interviewed", "offered", "hired"]
CandidateSource = Literal["email", "upload", "linkedin", "hrms", "referral"]


class CandidateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    location: str | None = Field(default=None, max_length=255)
    source: CandidateSource | None = None
    status: CandidateStatus = "applied"


class CandidateUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    location: str | None = Field(default=None, max_length=255)
    source: CandidateSource | None = None
    status: CandidateStatus | None = None


class CandidateResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr | None
    phone: str | None
    location: str | None
    source: CandidateSource | None
    status: CandidateStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateListResponse(BaseModel):
    items: list[CandidateResponse]
    total: int
    page: int
    size: int
