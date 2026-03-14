import importlib
from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("sqlalchemy")


def _make_candidate(**kwargs):
    candidate = MagicMock()
    candidate.id = kwargs.get("id", "cand-001")
    candidate.name = kwargs.get("name", "Test User")
    candidate.status = kwargs.get("status", "active")
    candidate.merged_into = kwargs.get("merged_into", None)
    candidate.all_experience = kwargs.get("all_experience", [])
    candidate.skills = kwargs.get("skills", ["Python", "Docker"])
    candidate.sources = kwargs.get("sources", ["upload"])
    candidate.phone = kwargs.get("phone", None)
    candidate.location = kwargs.get("location", None)
    candidate.linkedin_url = kwargs.get("linkedin_url", None)
    candidate.github_url = kwargs.get("github_url", None)
    candidate.candidate_bio = kwargs.get("candidate_bio", None)
    candidate.suggested_merge_id = None
    return candidate


def test_different_roles_same_company_keeps_both_entries():
    merge_module = importlib.import_module("candidate.merge_service")
    primary = _make_candidate(
        id="p1",
        all_experience=[{"company": "Acme", "role": "Backend Eng", "duration": "2y"}],
    )
    secondary = _make_candidate(
        id="s1",
        all_experience=[{"company": "Acme", "role": "Platform Eng", "duration": "1y"}],
    )

    db = MagicMock()
    db.execute.return_value.scalar_one_or_none.side_effect = [primary, secondary]
    db.refresh.return_value = None

    with patch.object(merge_module.asyncio, "run"), patch.object(
        merge_module, "normalize_skills", side_effect=lambda values: values
    ):
        result = merge_module.merge_candidates("p1", "s1", db)

    assert result["experience_count"] == 2


def test_merge_already_merged_secondary_raises_409_value_error():
    merge_module = importlib.import_module("candidate.merge_service")
    secondary = _make_candidate(id="s1", status="merged", merged_into="other")
    primary = _make_candidate(id="p1")
    db = MagicMock()
    db.execute.return_value.scalar_one_or_none.side_effect = [primary, secondary]

    with pytest.raises(ValueError, match="already merged"):
        merge_module.merge_candidates("p1", "s1", db)


def test_identical_ids_raises_value_error():
    merge_module = importlib.import_module("candidate.merge_service")

    with pytest.raises(ValueError, match="itself"):
        merge_module.merge_candidates("same", "same", MagicMock())


def test_merge_combines_sources_and_preserves_primary_fields():
    merge_module = importlib.import_module("candidate.merge_service")
    primary = _make_candidate(
        id="p1",
        sources=["gmail", "upload"],
        phone="111-1111",
        location="Bangalore",
        all_experience=[{"company": "Acme", "role": "Backend Eng", "duration": "2y"}],
    )
    secondary = _make_candidate(
        id="s1",
        sources=["upload", "linkedin"],
        phone="999-9999",
        location="Mumbai",
        all_experience=[{"company": "Beta", "role": "Platform Eng", "duration": "1y"}],
    )

    db = MagicMock()
    db.execute.return_value.scalar_one_or_none.side_effect = [primary, secondary]
    db.refresh.return_value = None

    with patch.object(merge_module, "_reindex_candidate_sync", return_value=None), patch.object(
        merge_module, "normalize_skills", side_effect=lambda values: values
    ):
        result = merge_module.merge_candidates("p1", "s1", db)

    assert result["ok"] is True
    assert set(primary.sources) == {"gmail", "upload", "linkedin"}
    assert primary.phone == "111-1111"
    assert primary.location == "Bangalore"

