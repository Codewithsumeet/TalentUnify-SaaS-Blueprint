from ai.fraud_detector import (
    SKILL_COUNT_THRESHOLDS,
    _check_keyword_stuffing,
    _sum_traceable_years,
    detect_fraud,
)


def test_keyword_density_counts_occurrences_not_unique_presence():
    """skill_hits must count each occurrence, not just whether skill appears"""
    candidate = {
        "skills": ["Python"],
        "experience_years": 5,
        "experience_level": "Mid",
        "all_experience": [],
        "raw_text": "Python " * 10 + " ".join(["word"] * 100),
    }
    signals = _check_keyword_stuffing(candidate)
    assert not any(signal.type == "keyword_stuffing" for signal in signals)

    candidate["raw_text"] = "Python " * 20 + " ".join(["word"] * 100)
    signals = _check_keyword_stuffing(candidate)
    assert any(signal.type == "keyword_stuffing" for signal in signals)


def test_skill_thresholds_below_parse_cap():
    """All flag thresholds must be < 25 (the parse cap)."""
    for level, threshold in SKILL_COUNT_THRESHOLDS.items():
        assert threshold["flag"] < 25, f"{level} flag threshold {threshold['flag']} >= parse cap 25"


def test_advanced_tech_check_case_insensitive():
    """'KUBERNETES' and 'kubernetes' both trigger advanced tech signal."""
    candidate = {
        "skills": ["KUBERNETES", "TERRAFORM"],
        "experience_years": 0,
        "experience_level": "Fresher",
        "all_experience": [],
        "raw_text": "",
    }
    result = detect_fraud(candidate)
    signals = [signal for signal in result["fraud_signals"] if signal["type"] == "skill_inflation"]
    assert any("enterprise" in signal["description"].lower() for signal in signals)


def test_duration_parser_handles_multiple_formats():
    experiences = [
        {"duration": "3y2m"},
        {"duration": "3 years 2 months"},
        {"duration": "Jan 2020 – Mar 2023"},
        {"duration": "(38m)"},
        {"duration": "3yrs"},
    ]
    for experience in experiences:
        total = _sum_traceable_years([experience])
        assert total >= 0, f"Negative result for duration: {experience['duration']}"
        assert total < 50, f"Implausibly large result for: {experience['duration']}"


def test_clean_candidate_scores_low_risk():
    candidate = {
        "name": "Clean Candidate",
        "skills": ["Python", "FastAPI", "Docker"],
        "experience_years": 5,
        "experience_level": "Mid",
        "all_experience": [
            {"company": "Acme", "role": "Engineer", "duration": "3y"},
            {"company": "Beta", "role": "Engineer", "duration": "2y"},
        ],
        "raw_text": "Python FastAPI Docker PostgreSQL " + "word " * 200,
    }
    result = detect_fraud(candidate)
    assert result["fraud_risk"] == "low"

