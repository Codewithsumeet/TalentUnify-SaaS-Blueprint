"""
Direct Gmail API integration (alternative to n8n).
Use this if you want TalentFlow to poll Gmail directly without n8n.
Requires GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET in .env.
"""
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from tasks.resume_tasks import parse_resume_task
from config import get_settings

settings = get_settings()
SCOPES   = ["https://www.googleapis.com/auth/gmail.readonly"]
RESUME_KEYWORDS = (
    "resume",
    "cv",
    "curriculum vitae",
    "application",
    "job",
    "hiring",
    "candidate",
    "profile",
    "experience",
)


def _keyword_score(text: str) -> float:
    value = (text or "").lower()
    hits = sum(1 for keyword in RESUME_KEYWORDS if keyword in value)
    if hits >= 4:
        return 2.0
    if hits == 3:
        return 1.5
    if hits == 2:
        return 1.0
    if hits == 1:
        return 0.5
    return 0.0


def _resume_threshold_score(subject: str, snippet: str, filename: str, mime_type: str) -> float:
    score = _keyword_score(subject) + _keyword_score(snippet)
    lower_name = (filename or "").lower()
    lower_mime = (mime_type or "").lower()
    if lower_name.endswith(".pdf") or "pdf" in lower_mime:
        score += 1.0
    if lower_name.endswith(".docx") or "wordprocessingml.document" in lower_mime:
        score += 1.0
    if "resume" in lower_name or "cv" in lower_name:
        score += 0.5
    return round(score, 2)


def poll_gmail_for_resumes(credentials_dict: dict) -> list[str]:
    """
    Polls Gmail for unread emails with PDF or DOCX attachments.
    credentials_dict: OAuth2 credentials from your auth flow.
    Returns: list of task_ids for queued parse jobs.
    """
    creds   = Credentials(**credentials_dict)
    service = build("gmail", "v1", credentials=creds)

    query    = "label:Recruitment is:unread has:attachment (filename:pdf OR filename:docx)"
    messages = service.users().messages().list(userId="me", q=query).execute()
    task_ids = []

    for msg_stub in (messages.get("messages") or []):
        msg = service.users().messages().get(
            userId="me", id=msg_stub["id"], format="full"
        ).execute()
        headers = msg.get("payload", {}).get("headers", []) or []
        header_map = {str(item.get("name", "")).lower(): str(item.get("value", "")) for item in headers}
        subject = header_map.get("subject", "")
        snippet = str(msg.get("snippet") or "")

        for part in (msg.get("payload", {}).get("parts") or []):
            filename  = part.get("filename", "")
            mime_type = part.get("mimeType", "")

            is_resume_file = (
                filename.lower().endswith(".pdf") or
                filename.lower().endswith(".docx")
            )
            if not is_resume_file:
                continue

            threshold_score = _resume_threshold_score(subject, snippet, filename, mime_type)
            if threshold_score < float(settings.gmail_resume_threshold):
                continue

            body = part.get("body", {})
            if "attachmentId" not in body:
                continue

            attachment = service.users().messages().attachments().get(
                userId="me",
                messageId=msg_stub["id"],
                id=body["attachmentId"],
            ).execute()

            file_bytes = base64.urlsafe_b64decode(attachment["data"] + "==")
            task       = parse_resume_task.delay(
                file_bytes = file_bytes,
                mime_type  = mime_type,
                source     = "gmail",
                filename   = filename,
                metadata   = {
                    "gmail_message_id": msg_stub["id"],
                    "threshold_score": threshold_score,
                    "subject": subject,
                },
            )
            task_ids.append(task.id)

        # Mark as read
        service.users().messages().modify(
            userId="me",
            id=msg_stub["id"],
            body={"removeLabelIds": ["UNREAD"]},
        ).execute()

    return task_ids
