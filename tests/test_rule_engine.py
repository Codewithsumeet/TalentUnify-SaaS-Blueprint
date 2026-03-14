from shortlist.rule_engine import ShortlistRuleConfig, evaluate_candidate, run_all_rules

RULE = ShortlistRuleConfig(
    id="r1",
    name="Senior Go",
    role_target="Backend",
    min_score=70,
    required_skills=["Go", "Kafka"],
    any_of_skills=["Redis", "PostgreSQL"],
    min_experience_years=5.0,
    location_filter="Bangalore",
    level_filter=["Senior"],
    auto_apply=True,
    priority=10,
)


def test_missing_required_skill_hard_disqualifies():
    candidate = {"ai_score": 90, "skills": ["Python"], "experience_years": 6, "location": "Bangalore"}
    result = evaluate_candidate(candidate, RULE)
    assert result["matches"] is False
    assert result["auto_shortlist"] is False


def test_wrong_location_is_soft_penalty_not_disqualifier():
    candidate = {
        "ai_score": 90,
        "skills": ["Go", "Kafka", "Redis"],
        "experience_years": 6,
        "location": "Mumbai",
    }
    result = evaluate_candidate(candidate, RULE)
    assert result["component_scores"]["location"] == 0.40


def test_weighted_score_in_range():
    candidate = {
        "ai_score": 85,
        "skills": ["Go", "Kafka", "Redis"],
        "experience_years": 6,
        "location": "Bangalore",
    }
    result = evaluate_candidate(candidate, RULE)
    assert 0 <= result["rule_score"] <= 100


def test_only_highest_priority_rule_sets_auto_shortlist():
    high_rule = ShortlistRuleConfig(
        id="rH",
        name="High Priority",
        role_target="",
        min_score=60,
        required_skills=[],
        any_of_skills=[],
        min_experience_years=0,
        location_filter=None,
        level_filter=[],
        auto_apply=True,
        priority=100,
    )
    low_rule = ShortlistRuleConfig(
        id="rL",
        name="Low Priority",
        role_target="",
        min_score=60,
        required_skills=[],
        any_of_skills=[],
        min_experience_years=0,
        location_filter=None,
        level_filter=[],
        auto_apply=True,
        priority=1,
    )
    candidate = {"ai_score": 90, "skills": ["Python"], "experience_years": 3, "location": "Bangalore"}
    results = run_all_rules(candidate, [low_rule, high_rule])
    auto_claims = [result for result in results if result.get("auto_shortlist")]
    assert len(auto_claims) == 1
    assert auto_claims[0]["rule_id"] == "rH"

