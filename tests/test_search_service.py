import asyncio
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace

from search import search_svc


class _FakeScalars:
    def __init__(self, candidates):
        self._candidates = candidates

    def all(self):
        return self._candidates


class _FakeExecuteResult:
    def __init__(self, candidates):
        self._candidates = candidates

    def scalars(self):
        return _FakeScalars(self._candidates)


class _FakeDb:
    def __init__(self, candidates):
        self._candidates = candidates

    async def execute(self, *_args, **_kwargs):
        return _FakeExecuteResult(self._candidates)


def _candidate(candidate_id: str):
    return SimpleNamespace(
        id=uuid.UUID(candidate_id),
        status="active",
        name="Database Candidate",
        current_role="Backend Engineer",
        current_company="TalentFlow",
        location="Bangalore",
        experience_years=4.0,
        experience_level="Senior",
        skills=["Python", "FastAPI"],
        sources=["upload"],
        candidate_bio="Built scalable hiring systems",
        fraud_risk="low",
        fraud_score=12,
        fraud_signals=[],
    )


def test_semantic_search_joins_db_candidate_data(monkeypatch):
    candidate_id = str(uuid.uuid4())

    async def _fake_embedding(_query):
        return [0.1, 0.2]

    async def _fake_query_index(*_args, **_kwargs):
        return SimpleNamespace(
            matches=[
                SimpleNamespace(
                    id=candidate_id,
                    score=0.91,
                    metadata={
                        "name": "Metadata Candidate",
                        "current_role": "Wrong Role",
                        "skills": ["Wrong Skill"],
                    },
                )
            ]
        )

    @asynccontextmanager
    async def _fake_get_db():
        yield _FakeDb([_candidate(candidate_id)])

    monkeypatch.setattr(search_svc, "get_embedding", _fake_embedding)
    monkeypatch.setattr(search_svc, "query_index", _fake_query_index)
    monkeypatch.setattr(search_svc, "get_db", _fake_get_db)
    monkeypatch.setattr(search_svc, "compute_match_breakdown", lambda **_kwargs: {"matched_skills": 2})

    results = asyncio.run(search_svc.semantic_search("senior python engineer", top_k=1))

    assert len(results) == 1
    first = results[0]
    assert first["candidate_id"] == candidate_id
    assert first["score"] == 91
    assert first["name"] == "Database Candidate"
    assert first["current_role"] == "Backend Engineer"
    assert first["skills"] == ["Python", "FastAPI"]
    assert first["match_breakdown"] == {"matched_skills": 2}


def test_semantic_search_falls_back_to_metadata_when_db_candidate_missing(monkeypatch):
    candidate_id = str(uuid.uuid4())

    async def _fake_embedding(_query):
        return [0.1, 0.2]

    async def _fake_query_index(*_args, **_kwargs):
        return SimpleNamespace(
            matches=[
                SimpleNamespace(
                    id=candidate_id,
                    score=0.77,
                    metadata={
                        "name": "Metadata Candidate",
                        "current_role": "ML Engineer",
                        "current_company": "Vector Labs",
                        "location": "Mumbai",
                        "experience_years": 3,
                        "experience_level": "Mid",
                        "skills": ["PyTorch", "Python"],
                        "sources": ["linkedin"],
                        "candidate_bio": "Focused on ranking and retrieval",
                        "fraud_risk": "medium",
                        "fraud_score": 45,
                        "fraud_signals": ["Email-domain mismatch"],
                    },
                )
            ]
        )

    @asynccontextmanager
    async def _fake_get_db():
        yield _FakeDb([])

    monkeypatch.setattr(search_svc, "get_embedding", _fake_embedding)
    monkeypatch.setattr(search_svc, "query_index", _fake_query_index)
    monkeypatch.setattr(search_svc, "get_db", _fake_get_db)
    monkeypatch.setattr(search_svc, "compute_match_breakdown", lambda **_kwargs: {"matched_skills": 1})

    results = asyncio.run(search_svc.semantic_search("ml engineer mumbai", top_k=1))

    assert len(results) == 1
    first = results[0]
    assert first["candidate_id"] == candidate_id
    assert first["score"] == 77
    assert first["name"] == "Metadata Candidate"
    assert first["current_role"] == "ML Engineer"
    assert first["fraud_risk"] == "medium"
