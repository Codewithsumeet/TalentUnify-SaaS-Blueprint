from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import get_candidate_service, get_current_user
from candidate.schemas import (
    CandidateCreate,
    CandidateListResponse,
    CandidateResponse,
    CandidateUpdate,
)
from candidate.service import CandidateService
from db.models import User

router = APIRouter(prefix="/api/v1/candidates", tags=["candidates"])


@router.get("", response_model=CandidateListResponse)
async def list_candidates(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, min_length=1, max_length=120),
    _: User = Depends(get_current_user),
    service: CandidateService = Depends(get_candidate_service),
) -> CandidateListResponse:
    return await service.list_candidates(page=page, size=size, search=search)


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: UUID,
    _: User = Depends(get_current_user),
    service: CandidateService = Depends(get_candidate_service),
) -> CandidateResponse:
    return await service.get_candidate(candidate_id)


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_candidate(
    payload: CandidateCreate,
    _: User = Depends(get_current_user),
    service: CandidateService = Depends(get_candidate_service),
) -> CandidateResponse:
    return await service.create_candidate(payload)


@router.patch("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: UUID,
    payload: CandidateUpdate,
    _: User = Depends(get_current_user),
    service: CandidateService = Depends(get_candidate_service),
) -> CandidateResponse:
    return await service.update_candidate(candidate_id=candidate_id, payload=payload)
