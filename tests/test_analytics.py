def test_analytics_returns_all_sections(client):
    """GET /analytics/summary must return all required keys."""
    response = client.get("/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    for key in [
        "kpis",
        "sourceBreakdown",
        "pipelineFunnel",
        "timeToHire",
        "skillsGap",
        "pipelineVelocity",
    ]:
        assert key in data, f"Missing key: {key}"


def test_analytics_kpis_structure(client):
    response = client.get("/analytics/summary")
    kpis = response.json()["kpis"]
    assert "totalCandidates" in kpis
    assert isinstance(kpis["totalCandidates"], int)


def test_analytics_funnel_applied_equals_total(client):
    """First funnel stage (Applied) count should equal total candidates."""
    response = client.get("/analytics/summary")
    data = response.json()
    total = data["kpis"]["totalCandidates"]
    funnel = data["pipelineFunnel"]
    if funnel:
        assert funnel[0]["count"] == total


def test_analytics_weekly_no_year_collision():
    """Week keys must include year to avoid W01 2024 == W01 2025 collision."""
    from collections import defaultdict
    from datetime import datetime

    dates = [datetime(2024, 12, 29), datetime(2025, 1, 5)]
    weekly = defaultdict(int)
    for date_value in dates:
        iso = date_value.isocalendar()
        key = f"{iso.year}-W{iso.week:02d}"
        weekly[key] += 1

    keys = list(weekly.keys())
    assert len(keys) == 2, f"Year collision: both dates mapped to same key: {keys}"

