import os

from celery import Celery
from celery.schedules import crontab
from config import get_settings

settings = get_settings()

celery_app = Celery(
    "talentflow",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["tasks.resume_tasks", "tasks.shortlist_tasks"],
)

celery_config = dict(
    task_serializer    = "json",
    result_serializer  = "json",
    accept_content     = ["json"],
    timezone           = "UTC",
    enable_utc         = True,
    task_track_started = True,
    task_acks_late     = True,
    worker_prefetch_multiplier = 1,  # one task at a time per worker (heavy AI models)
)

if os.name == "nt":
    # Celery prefork is not supported on native Windows workers.
    celery_config["worker_pool"] = "solo"
    celery_config["worker_concurrency"] = 1

celery_app.conf.update(**celery_config)

celery_app.conf.beat_schedule = {
    "run-shortlist-every-15-min": {
        "task": "tasks.shortlist_tasks.run_shortlist_periodic",
        "schedule": crontab(minute="*/15"),
    }
}
