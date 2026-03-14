"""
SSE endpoint: GET /events/{upload_id}

Frontend subscribes immediately after file upload:
  const es = new EventSource(`/events/${taskId}`)
  es.onmessage = (e) => updateUI(JSON.parse(e.data))

Status states pushed:
  uploading  → shows progress bar 0→80% in 400ms (optimistic)
  parsing    → shows skeleton shimmer card with step description
  complete   → skeleton fades out, real card fades in with green border flash
  failed     → error card with retry button — never blank, never silent
  duplicate  → notification: "Already in your database" with link to existing profile
"""
import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from config import get_settings

router   = APIRouter()
settings = get_settings()


@router.get("/events/{upload_id}")
async def stream_parse_status(upload_id: str):
    """Real-time parse status stream via Server-Sent Events."""

    async def event_generator():
        # Immediate optimistic feedback — shows "uploading" instantly
        yield f'data: {json.dumps({"status": "uploading"})}\n\n'
        await asyncio.sleep(0.15)

        import redis as redis_lib
        r = redis_lib.from_url(settings.redis_url, decode_responses=True)

        # Poll Redis for status updates (every 0.5s, max 60s)
        for _ in range(120):
            try:
                raw = r.get(f"task_status:{upload_id}")
            except Exception:
                raw = None

            if raw:
                try:
                    payload = json.loads(raw)
                except Exception:
                    payload = {"status": "parsing"}

                yield f'data: {json.dumps(payload)}\n\n'

                # Terminal states: stop streaming
                if payload.get("status") in ("complete", "failed", "duplicate"):
                    return
            else:
                yield f'data: {json.dumps({"status": "parsing"})}\n\n'

            await asyncio.sleep(0.5)

        # Timeout fallback
        yield f'data: {json.dumps({"status": "failed", "reason": "timeout"})}\n\n'

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control":    "no-cache",
            "X-Accel-Buffering":"no",
            "Connection":       "keep-alive",
        },
    )
