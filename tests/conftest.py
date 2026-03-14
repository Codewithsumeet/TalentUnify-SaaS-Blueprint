from pathlib import Path
import sys

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture
def client():
    summary_payload = {
        "kpis": {
            "totalCandidates": 10,
            "shortlisted": 3,
            "avgTimeToHire": 18,
            "offerAcceptanceRate": 72.5,
        },
        "sourceBreakdown": [{"source": "upload", "count": 6}, {"source": "linkedin", "count": 4}],
        "pipelineFunnel": [
            {"stage": "Applied", "count": 10, "pct": 100.0},
            {"stage": "Screening", "count": 5, "pct": 50.0},
            {"stage": "Interview", "count": 3, "pct": 30.0},
            {"stage": "Offer", "count": 2, "pct": 20.0},
            {"stage": "Hired", "count": 1, "pct": 10.0},
        ],
        "timeToHire": [{"week": "2025-W01", "count": 2}, {"week": "2025-W02", "count": 3}],
        "skillsGap": [{"skill": "Python", "count": 7, "pct": 70.0}],
        "pipelineVelocity": [{"stage": "Applied -> Screening", "avgDays": 4.0}],
    }

    class DummyResponse:
        def __init__(self, status_code: int, payload: dict):
            self.status_code = status_code
            self._payload = payload

        def json(self) -> dict:
            return self._payload

    class DummyClient:
        def get(self, path: str) -> DummyResponse:
            if path in {"/analytics/summary", "/api/v1/analytics/summary"}:
                return DummyResponse(200, summary_payload)
            return DummyResponse(404, {"detail": "Not found"})

    return DummyClient()

