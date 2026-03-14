"""
Outlook recruitment watcher scaffold.

This module provides the polling workflow for Microsoft Graph mailbox intake.
It is intentionally local/dev friendly and can be extended into a scheduled task.
"""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass

import httpx

from tasks.resume_tasks import parse_resume_task


@dataclass
class OutlookAttachment:
    filename: str
    content_type: str
    content_bytes: bytes
    sender_email: str | None = None
    message_id: str | None = None


class OutlookRecruitmentWatcher:
    """Polls Outlook Inbox via Microsoft Graph and queues PDF resumes."""

    GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

    def __init__(self, access_token: str | None = None, mailbox: str = "me", folder: str = "Inbox"):
        self.access_token = access_token or os.getenv("MS_GRAPH_ACCESS_TOKEN", "")
        self.mailbox = mailbox
        self.folder = folder

    @property
    def enabled(self) -> bool:
        return bool(self.access_token)

    async def fetch_unread_pdf_attachments(self, limit: int = 10) -> list[OutlookAttachment]:
        if not self.enabled:
            return []

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
        query = (
            f"{self.GRAPH_BASE_URL}/{self.mailbox}/mailFolders/{self.folder}/messages"
            "?$select=id,subject,from,hasAttachments,isRead&$top="
            f"{max(1, min(limit, 50))}&$filter=isRead eq false and hasAttachments eq true"
        )

        attachments: list[OutlookAttachment] = []
        async with httpx.AsyncClient(timeout=25.0, headers=headers) as client:
            response = await client.get(query)
            response.raise_for_status()
            for message in response.json().get("value", []):
                message_id = message.get("id")
                if not message_id:
                    continue
                sender = (((message.get("from") or {}).get("emailAddress") or {}).get("address"))
                attachment_url = f"{self.GRAPH_BASE_URL}/{self.mailbox}/messages/{message_id}/attachments"
                attachment_resp = await client.get(attachment_url)
                attachment_resp.raise_for_status()
                for item in attachment_resp.json().get("value", []):
                    filename = (item.get("name") or "").strip()
                    content_type = (item.get("contentType") or "").lower()
                    is_pdf = filename.lower().endswith(".pdf") or content_type == "application/pdf"
                    if not is_pdf:
                        continue
                    raw_content = item.get("contentBytes")
                    if not raw_content:
                        continue
                    try:
                        payload = base64.b64decode(raw_content)
                    except Exception:
                        continue
                    attachments.append(
                        OutlookAttachment(
                            filename=filename or "outlook_resume.pdf",
                            content_type="application/pdf",
                            content_bytes=payload,
                            sender_email=sender,
                            message_id=message_id,
                        )
                    )
        return attachments

    def queue_resume(self, attachment: OutlookAttachment) -> str:
        task = parse_resume_task.delay(
            file_bytes=attachment.content_bytes,
            mime_type=attachment.content_type,
            source="outlook",
            filename=attachment.filename,
            metadata={
                "source_system": "outlook_graph",
                "sender_email": attachment.sender_email,
                "message_id": attachment.message_id,
            },
        )
        return task.id

    async def poll_once(self, limit: int = 10) -> dict:
        attachments = await self.fetch_unread_pdf_attachments(limit=limit)
        queued = [self.queue_resume(attachment) for attachment in attachments]
        return {"fetched": len(attachments), "queued": len(queued), "task_ids": queued}
