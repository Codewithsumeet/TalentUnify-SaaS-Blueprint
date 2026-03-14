from pathlib import Path
from uuid import UUID

from celery.result import AsyncResult
from fastapi import UploadFile

from app.exceptions import NotFoundException, ValidationException
from resume.parser import DOCX_MIME_TYPE, PDF_MIME_TYPE
from resume.repository import ResumeRepository
from resume.schemas import (
    ResumeResponse,
    ResumeStatusResponse,
    ResumeTaskResult,
    ResumeUploadResponse,
)
from tasks.celery_app import celery_app
from tasks.resume_tasks import parse_resume_task

MAX_UPLOAD_SIZE_BYTES = 25 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_MIME_TYPES = {PDF_MIME_TYPE, DOCX_MIME_TYPE}


class ResumeService:
    def __init__(self, repository: ResumeRepository) -> None:
        self.repository = repository

    async def enqueue_resume_upload(self, file: UploadFile) -> ResumeUploadResponse:
        if not file.filename:
            raise ValidationException("File name is required")

        extension = Path(file.filename).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationException("Only PDF and DOCX files are allowed")

        file_bytes = await file.read()
        if not file_bytes:
            raise ValidationException("Uploaded file is empty")
        if len(file_bytes) > MAX_UPLOAD_SIZE_BYTES:
            raise ValidationException("File exceeds 25MB upload limit")

        mime_type = file.content_type or ""
        if mime_type and mime_type not in ALLOWED_MIME_TYPES:
            raise ValidationException("Unsupported file content type")
        if not mime_type:
            mime_type = PDF_MIME_TYPE if extension == ".pdf" else DOCX_MIME_TYPE

        task = parse_resume_task.delay(
            file_bytes=file_bytes,
            mime_type=mime_type,
            source="upload",
            filename=file.filename,
            metadata={},
        )
        return ResumeUploadResponse(task_id=task.id, status="queued")

    async def get_task_status(self, task_id: str) -> ResumeStatusResponse:
        result = AsyncResult(task_id, app=celery_app)

        if result.status in {"PENDING"}:
            return ResumeStatusResponse(task_id=task_id, status="queued")

        if result.status in {"RECEIVED", "STARTED", "RETRY"}:
            return ResumeStatusResponse(task_id=task_id, status="processing")

        if result.status == "SUCCESS":
            task_result = ResumeTaskResult.model_validate(result.result)
            return ResumeStatusResponse(
                task_id=task_id,
                status="parsed",
                result=task_result,
            )

        return ResumeStatusResponse(
            task_id=task_id,
            status="failed",
            error=str(result.result) if result.result else "Task failed",
        )

    async def get_resume(self, resume_id: UUID) -> ResumeResponse:
        resume = await self.repository.get_resume(resume_id)
        if not resume:
            raise NotFoundException(f"Resume {resume_id} not found")
        return ResumeResponse.model_validate(resume)
