from celery.utils.log import get_task_logger
from sqlalchemy import select

from database import get_db_context
from models.candidate import Candidate
from models.shortlist_rule import ShortlistRule
from shortlist.rule_engine import ShortlistRuleConfig, run_all_rules
from tasks.celery_app import celery_app

logger = get_task_logger(__name__)


def _to_config(rule: ShortlistRule) -> ShortlistRuleConfig:
    return ShortlistRuleConfig(
        id=rule.id,
        name=rule.name,
        role_target=rule.role_target or "",
        min_score=rule.min_score or 70,
        required_skills=rule.required_skills or [],
        any_of_skills=rule.any_of_skills or [],
        min_experience_years=rule.min_experience_years or 0.0,
        location_filter=rule.location_filter,
        level_filter=rule.level_filter or [],
        auto_apply=bool(rule.auto_apply),
        priority=rule.priority or 0,
    )


@celery_app.task(name="tasks.shortlist_tasks.run_shortlist_periodic")
def run_shortlist_periodic() -> dict:
    with get_db_context() as db:
        rules = db.execute(
            select(ShortlistRule)
            .where(ShortlistRule.is_active.is_(True))
            .order_by(ShortlistRule.priority.desc(), ShortlistRule.created_at.desc())
        ).scalars().all()
        if not rules:
            return {"total_candidates": 0, "matched": 0, "auto_shortlisted": 0, "updated_candidate_ids": []}

        configs = [_to_config(rule) for rule in rules]
        rule_match_counts = {rule.id: 0 for rule in rules}
        candidates = db.execute(select(Candidate).where(Candidate.status == "active")).scalars().all()

        matched = 0
        auto_shortlisted = 0
        updated_ids: list[str] = []

        for candidate in candidates:
            evaluations = run_all_rules(candidate.to_dict(), configs)
            matches = [evaluation for evaluation in evaluations if evaluation.get("matches")]
            if not matches:
                candidate.shortlisted = False
                candidate.shortlist_rule_id = None
                continue

            matched += 1
            best = max(matches, key=lambda item: (item["rule_score"], item["priority"]))
            candidate.shortlisted = True
            candidate.shortlist_rule_id = best["rule_id"]
            updated_ids.append(str(candidate.id))
            rule_match_counts[best["rule_id"]] = rule_match_counts.get(best["rule_id"], 0) + 1

            if any(item.get("auto_shortlist") for item in matches):
                auto_shortlisted += 1

        for rule in rules:
            rule.match_count = rule_match_counts.get(rule.id, 0)

        logger.info(
            "Shortlist run complete",
            extra={
                "total_candidates": len(candidates),
                "matched": matched,
                "auto_shortlisted": auto_shortlisted,
            },
        )
        return {
            "total_candidates": len(candidates),
            "matched": matched,
            "auto_shortlisted": auto_shortlisted,
            "updated_candidate_ids": updated_ids,
        }

