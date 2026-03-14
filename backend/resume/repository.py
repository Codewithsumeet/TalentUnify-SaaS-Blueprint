from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Resume


class ResumeRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_resume(self, resume_id: UUID) -> Resume | None:
        return await self.db.get(Resume, resume_id)
