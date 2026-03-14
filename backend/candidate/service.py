from uuid import UUID

from app.exceptions import ConflictException, NotFoundException
from candidate.repository import CandidateRepository
from candidate.schemas import (
    CandidateCreate,
    CandidateListResponse,
    CandidateResponse,
    CandidateUpdate,
)


class CandidateService:
    def __init__(self, repository: CandidateRepository) -> None:
        self.repository = repository

    async def list_candidates(
        self,
        *,
        page: int,
        size: int,
        search: str | None,
    ) -> CandidateListResponse:
        items, total = await self.repository.list_candidates(
            page=page,
            size=size,
            search=search,
        )
        return CandidateListResponse(
            items=[CandidateResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            size=size,
        )

    async def get_candidate(self, candidate_id: UUID) -> CandidateResponse:
        candidate = await self.repository.get_by_id(candidate_id)
        if not candidate:
            raise NotFoundException(f"Candidate {candidate_id} not found")
        return CandidateResponse.model_validate(candidate)

    async def create_candidate(self, payload: CandidateCreate) -> CandidateResponse:
        if payload.email:
            existing = await self.repository.get_by_email(str(payload.email))
            if existing:
                raise ConflictException("Candidate with this email already exists")

        candidate = await self.repository.create(payload)
        return CandidateResponse.model_validate(candidate)

    async def update_candidate(
        self,
        *,
        candidate_id: UUID,
        payload: CandidateUpdate,
    ) -> CandidateResponse:
        candidate = await self.repository.get_by_id(candidate_id)
        if not candidate:
            raise NotFoundException(f"Candidate {candidate_id} not found")

        updates = payload.model_dump(exclude_unset=True)

        if "email" in updates and updates["email"]:
            existing = await self.repository.get_by_email(str(updates["email"]))
            if existing and existing.id != candidate.id:
                raise ConflictException("Candidate with this email already exists")

        updated = await self.repository.update(candidate, updates)
        return CandidateResponse.model_validate(updated)
