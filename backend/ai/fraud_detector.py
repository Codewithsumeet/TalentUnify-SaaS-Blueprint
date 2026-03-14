"""
Tier 4 fraud detection. Pure Python, no external API calls.
Called after skill normalization and before DB write.
"""

import re
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Literal


@dataclass
class FraudSignal:
    type: str
    severity: Literal["low", "medium", "high"]
    description: str
    evidence: dict


SKILL_COUNT_THRESHOLDS: dict[str, dict[str, int]] = {
    "Fresher": {"warn": 10, "flag": 16},
    "Junior": {"warn": 14, "flag": 20},
    "Mid": {"warn": 16, "flag": 22},
    "Senior": {"warn": 18, "flag": 24},
    "Principal": {"warn": 19, "flag": 24},
}

ADVANCED_TECH: frozenset[str] = frozenset(
    {"kubernetes", "terraform", "kafka", "spark", "flink", "cassandra", "istio", "envoy", "ebpf"}
)

MONTH_MAP: dict[str, int] = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

TEMPLATE_PHRASES: list[str] = [
    "experience with agile methodologies",
    "strong communication and interpersonal skills",
    "team player with excellent problem-solving",
    "passion for technology and innovation",
    "results-driven professional",
    "proficient in all aspects of software development",
    "self-motivated and detail-oriented",
    "excellent verbal and written communication",
]


def detect_fraud(candidate: dict) -> dict:
    signals: list[FraudSignal] = []
    signals.extend(_check_skill_inflation(candidate))
    signals.extend(_check_experience_gap(candidate))
    signals.extend(_check_keyword_stuffing(candidate))

    high = sum(1 for signal in signals if signal.severity == "high")
    medium = sum(1 for signal in signals if signal.severity == "medium")

    if high >= 1 or medium >= 2:
        risk = "high"
    elif medium >= 1:
        risk = "medium"
    else:
        risk = "low"

    return {
        "fraud_risk": risk,
        "fraud_score": {"low": 10, "medium": 45, "high": 80}[risk],
        "fraud_signals": [asdict(signal) for signal in signals],
    }


def _check_skill_inflation(candidate: dict) -> list[FraudSignal]:
    signals: list[FraudSignal] = []
    skills = candidate.get("skills") or []
    level = candidate.get("experience_level") or "Mid"
    experience_years = float(candidate.get("experience_years") or 0)
    threshold = SKILL_COUNT_THRESHOLDS.get(level, {"warn": 18, "flag": 22})

    if len(skills) >= threshold["flag"]:
        signals.append(
            FraudSignal(
                type="skill_inflation",
                severity="high",
                description=(
                    f"{len(skills)} skills listed for {level} "
                    f"({experience_years:.0f}yr) — verify depth in interview"
                ),
                evidence={
                    "skill_count": len(skills),
                    "level": level,
                    "exp_years": experience_years,
                },
            )
        )
    elif len(skills) >= threshold["warn"]:
        signals.append(
            FraudSignal(
                type="skill_inflation",
                severity="medium",
                description=f"{len(skills)} skills listed — confirm actual proficiency depth",
                evidence={"skill_count": len(skills), "level": level},
            )
        )

    if level == "Fresher":
        advanced = [skill for skill in skills if skill.lower() in ADVANCED_TECH]
        if len(advanced) >= 2:
            signals.append(
                FraudSignal(
                    type="skill_inflation",
                    severity="medium",
                    description=f"Fresher claims enterprise tools: {', '.join(advanced)}",
                    evidence={"advanced_skills": advanced},
                )
            )

    return signals


def _sum_traceable_years(all_experience: list[dict]) -> float:
    total_months = 0
    now_year = datetime.now().year
    now_month = datetime.now().month

    for experience in all_experience:
        duration = str(experience.get("duration") or "").lower().strip()
        if not duration:
            continue

        match_years_months = re.search(r"(\d+)\s*y(?:rs?|ears?)?\s*(?:(\d+)\s*m(?:onths?)?)?", duration)
        if match_years_months:
            years = int(match_years_months.group(1))
            months = int(match_years_months.group(2) or 0)
            total_months += years * 12 + months
            continue

        dates = re.findall(r"([a-z]{3})\s+(\d{4})", duration)
        if dates:
            start_month = MONTH_MAP.get(dates[0][0])
            start_year = int(dates[0][1])
            if start_month is None:
                continue
            if len(dates) >= 2:
                end_month = MONTH_MAP.get(dates[1][0], now_month)
                end_year = int(dates[1][1])
            else:
                end_year = now_year
                end_month = now_month
            span = (end_year - start_year) * 12 + (end_month - start_month)
            if 0 < span <= 480:
                total_months += span
            continue

        month_match = re.search(r"\((\d+)([ym])\)", duration)
        if month_match:
            value = int(month_match.group(1))
            unit = month_match.group(2)
            total_months += value * 12 if unit == "y" else value

    return round(total_months / 12, 1)


def _check_experience_gap(candidate: dict) -> list[FraudSignal]:
    signals: list[FraudSignal] = []
    claimed_years = float(candidate.get("experience_years") or 0)
    level = candidate.get("experience_level") or ""
    all_experience = candidate.get("all_experience") or []
    traceable = _sum_traceable_years(all_experience)

    if traceable > 0:
        gap = claimed_years - traceable
        if gap > 2.5:
            signals.append(
                FraudSignal(
                    type="experience_gap",
                    severity="high",
                    description=(
                        f"Claims {claimed_years:.0f}yr but timeline shows "
                        f"{traceable:.1f}yr traceable — {gap:.1f}yr unexplained"
                    ),
                    evidence={"claimed": claimed_years, "traceable": traceable, "gap": round(gap, 1)},
                )
            )
        elif gap > 1.5:
            signals.append(
                FraudSignal(
                    type="experience_gap",
                    severity="medium",
                    description=f"{gap:.1f}yr gap between claimed and traceable — verify dates",
                    evidence={"claimed": claimed_years, "traceable": traceable},
                )
            )

    level_minimums = {"Fresher": 0, "Junior": 0, "Mid": 2, "Senior": 5, "Principal": 10}
    minimum_for_level = level_minimums.get(level, 0)
    if level and minimum_for_level > 0 and claimed_years < minimum_for_level - 1:
        signals.append(
            FraudSignal(
                type="experience_gap",
                severity="medium",
                description=(
                    f"Claims {level} with {claimed_years:.0f}yr — "
                    f"minimum for this level is {minimum_for_level}yr"
                ),
                evidence={"level": level, "years": claimed_years, "minimum": minimum_for_level},
            )
        )

    return signals


def _check_keyword_stuffing(candidate: dict) -> list[FraudSignal]:
    signals: list[FraudSignal] = []
    raw_text = str(candidate.get("raw_text") or "")
    skills = candidate.get("skills") or []

    if not raw_text or not skills:
        return signals

    text_lower = raw_text.lower()
    all_words = re.findall(r"\b\w{4,}\b", text_lower)
    total_words = max(len(all_words), 1)

    skill_hits = sum(
        len(re.findall(r"\b" + re.escape(skill.lower()) + r"\b", text_lower))
        for skill in skills
    )
    density = skill_hits / total_words

    if total_words > 100 and density > 0.12:
        signals.append(
            FraudSignal(
                type="keyword_stuffing",
                severity="medium",
                description=f"Skill keyword density {density:.0%} (normal 3–8%) — possible ATS optimisation",
                evidence={
                    "density": round(density, 3),
                    "skill_hits": skill_hits,
                    "total_words": total_words,
                },
            )
        )

    template_hits = [phrase for phrase in TEMPLATE_PHRASES if phrase in text_lower]
    if len(template_hits) >= 2:
        signals.append(
            FraudSignal(
                type="keyword_stuffing",
                severity="low",
                description=f"{len(template_hits)} generic template phrases detected",
                evidence={"phrases": template_hits},
            )
        )

    return signals

