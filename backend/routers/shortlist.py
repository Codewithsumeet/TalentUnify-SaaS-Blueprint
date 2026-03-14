import sqlalchemy as sa
from fastapi import APIRouter
from pydantic import BaseModel, Field

from database import get_db
from models.candidate import Candidate
from models.shortlist_rule import ShortlistRule
from shortlist.rule_engine import ShortlistRuleConfig, run_all_rules

router = APIRouter(prefix="/api/v1/shortlist", tags=["shortlist"])


class ShortlistRuleCreate(BaseModel):
    name: str
    role_target: str | None = None
    min_score: int = Field(default=70, ge=0, le=100)
    required_skills: list[str] = Field(default_factory=list)
    any_of_skills: list[str] = Field(default_factory=list)
    min_experience_years: float = Field(default=0.0, ge=0.0)
    location_filter: str | None = None
    level_filter: list[str] = Field(default_factory=list)
    auto_apply: bool = False
    is_active: bool = True
    priority: int = 0
    created_by: str | None = None


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


def _serialize_rule(rule: ShortlistRule) -> dict:
    return {
        "id": rule.id,
        "name": rule.name,
        "role_target": rule.role_target,
        "min_score": rule.min_score,
        "required_skills": rule.required_skills or [],
        "any_of_skills": rule.any_of_skills or [],
        "min_experience_years": rule.min_experience_years,
        "location_filter": rule.location_filter,
        "level_filter": rule.level_filter or [],
        "auto_apply": bool(rule.auto_apply),
        "is_active": bool(rule.is_active),
        "priority": rule.priority,
        "match_count": rule.match_count,
        "created_at": rule.created_at.isoformat() if rule.created_at else None,
        "created_by": rule.created_by,
    }


async def _seed_default_rules_if_needed(db) -> None:
    existing_result = await db.execute(sa.select(sa.func.count()).select_from(ShortlistRule))
    if int(existing_result.scalar() or 0) > 0:
        return

    db.add_all(
        [
            ShortlistRule(
                name="Senior Backend Auto",
                role_target="Backend Engineer",
                min_score=75,
                required_skills=["Python", "FastAPI"],
                any_of_skills=["PostgreSQL", "Redis", "Kafka"],
                min_experience_years=4.0,
                location_filter="Bangalore",
                level_filter=["Senior", "Lead"],
                auto_apply=True,
                priority=90,
                created_by="system-seed",
            ),
            ShortlistRule(
                name="Frontend React Priority",
                role_target="Frontend Engineer",
                min_score=70,
                required_skills=["React"],
                any_of_skills=["TypeScript", "Next.js"],
                min_experience_years=2.0,
                auto_apply=False,
                priority=60,
                created_by="system-seed",
            ),
        ]
    )
    await db.flush()


@router.get("/rules")
async def list_rules():
    async with get_db() as db:
        await _seed_default_rules_if_needed(db)
        result = await db.execute(
            sa.select(ShortlistRule).order_by(ShortlistRule.priority.desc(), ShortlistRule.created_at.desc())
        )
        rules = result.scalars().all()
    return [_serialize_rule(rule) for rule in rules]


@router.post("/rules")
async def create_rule(payload: ShortlistRuleCreate):
    async with get_db() as db:
        rule = ShortlistRule(**payload.model_dump())
        db.add(rule)
        await db.commit()
        await db.refresh(rule)
    return _serialize_rule(rule)


@router.post("/run")
async def run_shortlist_now():
    async with get_db() as db:
        rules_result = await db.execute(
            sa.select(ShortlistRule)
            .where(ShortlistRule.is_active.is_(True))
            .order_by(ShortlistRule.priority.desc(), ShortlistRule.created_at.desc())
        )
        rules = rules_result.scalars().all()
        configs = [_to_config(rule) for rule in rules]
        rule_match_counts = {rule.id: 0 for rule in rules}

        candidates_result = await db.execute(
            sa.select(Candidate).where(Candidate.status == "active")
        )
        candidates = candidates_result.scalars().all()

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

        await db.commit()

    return {
        "total_candidates": len(candidates),
        "matched": matched,
        "auto_shortlisted": auto_shortlisted,
        "updated_candidate_ids": updated_ids,
    }

