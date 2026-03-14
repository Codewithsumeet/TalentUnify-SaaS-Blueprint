"""Celery task package."""

from pathlib import Path
import sys

backend_dir = Path(__file__).resolve().parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from .celery_app import celery_app as celery

__all__ = ["celery"]
