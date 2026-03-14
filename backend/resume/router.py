from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.dependencies import get_current_user, get_resume_service
from db.models import User
from resume.schemas import ResumeResponse, ResumeStatusResponse, ResumeUploadResponse
from resume.service import ResumeService

router = APIRouter(prefix="/api/v1/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(
    file: UploadFile = File(...),
    _: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
) -> ResumeUploadResponse:
    return await service.enqueue_resume_upload(file)


@router.get("/status/{task_id}", response_model=ResumeStatusResponse)
async def get_resume_status(
    task_id: str,
    _: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
) -> ResumeStatusResponse:
    return await service.get_task_status(task_id)


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: UUID,
    _: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
) -> ResumeResponse:
    return await service.get_resume(resume_id)
