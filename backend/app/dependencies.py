from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.repository import AuthRepository
from auth.service import AuthService
from candidate.repository import CandidateRepository
from candidate.service import CandidateService
from db.database import get_db_session
from db.models import User
from resume.repository import ResumeRepository
from resume.service import ResumeService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_auth_service(
    db: AsyncSession = Depends(get_db_session),
) -> AuthService:
    repository = AuthRepository(db)
    return AuthService(repository)


def get_candidate_service(
    db: AsyncSession = Depends(get_db_session),
) -> CandidateService:
    repository = CandidateRepository(db)
    return CandidateService(repository)


def get_resume_service(
    db: AsyncSession = Depends(get_db_session),
) -> ResumeService:
    repository = ResumeRepository(db)
    return ResumeService(repository)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    return await service.get_user_from_access_token(token)
