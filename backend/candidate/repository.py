from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from candidate.schemas import CandidateCreate
from db.models import Candidate


class CandidateRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_candidates(
        self,
        *,
        page: int,
        size: int,
        search: str | None,
    ) -> tuple[list[Candidate], int]:
        query = select(Candidate)
        count_query = select(func.count(Candidate.id))

        if search:
            search_term = f"%{search.strip()}%"
            filter_clause = or_(
                Candidate.name.ilike(search_term),
                Candidate.email.ilike(search_term),
            )
            query = query.where(filter_clause)
            count_query = count_query.where(filter_clause)

        query = query.order_by(Candidate.created_at.desc())
        query = query.offset((page - 1) * size).limit(size)

        result = await self.db.scalars(query)
        total = await self.db.scalar(count_query)
        return list(result), int(total or 0)

    async def get_by_id(self, candidate_id: UUID) -> Candidate | None:
        return await self.db.get(Candidate, candidate_id)

    async def get_by_email(self, email: str) -> Candidate | None:
        query = select(Candidate).where(Candidate.email == email)
        return await self.db.scalar(query)

    async def create(self, payload: CandidateCreate) -> Candidate:
        candidate = Candidate(**payload.model_dump())
        self.db.add(candidate)
        await self.db.commit()
        await self.db.refresh(candidate)
        return candidate

    async def update(
        self,
        candidate: Candidate,
        updates: dict[str, object],
    ) -> Candidate:
        for field, value in updates.items():
            setattr(candidate, field, value)

        await self.db.commit()
        await self.db.refresh(candidate)
        return candidate
