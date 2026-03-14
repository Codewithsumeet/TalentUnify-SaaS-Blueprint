"""
Webhook receiver for the n8n Pragnakalp Gmail workflow.

n8n workflow does:
  Gmail Trigger → IF has attachment → IF is_resume → Read Binary → HTTP POST here

This endpoint:
  Receives → decodes base64 → queues Celery parse_resume_task
"""
import base64
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/intake")


class N8nWebhookPayload(BaseModel):
    filename:     str
    mime_type:    str
    file_base64:  str
    sender_email: str | None = None
    subject:      str | None = None


@router.post("/gmail-webhook")
async def receive_n8n_webhook(payload: N8nWebhookPayload):
    """Receives base64-encoded resume from n8n, queues for processing."""
    try:
        file_bytes = base64.b64decode(payload.file_base64)
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid base64 encoding.")

    from tasks.resume_tasks import parse_resume_task

    task = parse_resume_task.delay(
        file_bytes = file_bytes,
        mime_type  = payload.mime_type,
        source     = "gmail",
        filename   = payload.filename,
        metadata   = {
            "sender_email": payload.sender_email,
            "subject":      payload.subject,
        },
    )
    return {"task_id": task.id, "status": "queued", "filename": payload.filename}
