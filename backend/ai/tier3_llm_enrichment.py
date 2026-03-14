"""
Tier 3: LLM enrichment via Claude 3.5 Haiku.
Model: claude-3-5-haiku-20241022
Cost:  ~$0.00025 per resume
"""
import json
import anthropic
from pydantic import BaseModel
from typing import Optional

from .normalize import normalize_skills
from config import get_settings

settings = get_settings()

# BUG FIX 3: correct, existing model string
MODEL = "claude-3-5-haiku-20241022"

SYSTEM = """You are a resume parsing engine.
Return ONLY a valid JSON object. No markdown fences. No preamble. No explanation.
Start with { and end with }.

Rules:
1. Return null for any field you cannot find — never invent data.
2. skills: extract ALL technical skills. Normalize aliases (JS→JavaScript, k8s→Kubernetes).
3. experience_years: total calendar span as float. Overlapping roles counted once. Max 50.
4. experience_level: exactly one of Fresher|Junior|Mid|Senior|Principal.
   Fresher=0-1yr, Junior=1-3yr, Mid=3-6yr, Senior=6-10yr, Principal=10+yr.
5. candidate_bio: 2 sentences, third-person English, max 60 words, facts only.
6. all_experience: array sorted most-recent-first. Each item: {company,role,duration,summary}.
7. certifications: names only, no issuer or dates.

Required output schema (replace nulls with actual values):
{"name":null,"email":null,"phone":null,"location":null,"linkedin_url":null,
"github_url":null,"current_role":null,"current_company":null,
"experience_years":null,"experience_level":null,"skills":[],
"all_experience":[],"certifications":[],"candidate_bio":null}"""


class ExperienceEntry(BaseModel):
    company:  str = ""
    role:     str = ""
    duration: str = ""
    summary:  str = ""


class ParsedCandidate(BaseModel):
    name:             Optional[str]             = None
    email:            Optional[str]             = None
    phone:            Optional[str]             = None
    location:         Optional[str]             = None
    linkedin_url:     Optional[str]             = None
    github_url:       Optional[str]             = None
    current_role:     Optional[str]             = None
    current_company:  Optional[str]             = None
    experience_years: Optional[float]           = None
    experience_level: Optional[str]             = None
    skills:           list[str]                 = []
    all_experience:   list[ExperienceEntry]     = []
    certifications:   list[str]                 = []
    candidate_bio:    Optional[str]             = None


def _strip_fences(text: str) -> str:
    """Strip accidental markdown code fences from LLM output."""
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text  = parts[1].lstrip("json").strip() if len(parts) > 1 else text
    start = text.find("{")
    if start > 0:
        text = text[start:]
    end = text.rfind("}")
    if end != -1 and end < len(text) - 1:
        text = text[:end + 1]
    return text


async def enrich(markdown: str, pre: dict) -> dict:
    """
    Main enrichment entry point.
    Returns ParsedCandidate dict on success.
    Returns best-effort partial dict with _parse_error key on failure.
    """
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    hints = "\n".join(
        f"  {k}: {v}"
        for k in ("email", "phone", "linkedin_url", "github_url")
        if (v := pre.get(k))
    )
    user_prompt = (
        f"Pre-extracted contact hints (prefer these if resume text is ambiguous):\n{hints}\n\n"
        f"--- RESUME TEXT ---\n{markdown[:8000]}\n--- END RESUME ---\n\n"
        "Return ONLY the JSON object."
    )

    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = _strip_fences(msg.content[0].text)
        parsed = json.loads(raw)

        try:
            validated = ParsedCandidate(**parsed)
            result    = validated.model_dump()
            # Convert ExperienceEntry objects to plain dicts
            result["all_experience"] = [
                e if isinstance(e, dict) else e.model_dump()
                for e in result["all_experience"]
            ]
        except Exception:
            # Pydantic rejected it — use raw parsed dict with defaults
            result = {k: parsed.get(k, v.default if hasattr(v, 'default') else None)
                      for k, v in ParsedCandidate.model_fields.items()}
            result.setdefault("skills", [])
            result.setdefault("all_experience", [])
            result.setdefault("certifications", [])

        # Merge regex-extracted contacts (more reliable for contact fields)
        for field in ("email", "phone", "linkedin_url", "github_url"):
            if pre.get(field) and not result.get(field):
                result[field] = pre[field]

        # Merge skills from all tiers
        all_skills = list(set(
            (result.get("skills") or []) +
            pre.get("skills_bert", []) +
            pre.get("skills_phase2", [])
        ))
        result["skills"] = normalize_skills(all_skills)

        # Clamp experience_years
        exp = result.get("experience_years")
        if exp is not None:
            result["experience_years"] = max(0.0, min(float(exp), 50.0))

        return result

    except Exception as exc:
        # Graceful degradation: return pre-extracted data + error flag
        fallback = {k: None for k in ParsedCandidate.model_fields}
        for k, v in pre.items():
            if k in fallback:
                fallback[k] = v
        fallback["skills"]         = normalize_skills(
            pre.get("skills_bert", []) + pre.get("skills_phase2", [])
        )
        fallback["all_experience"] = []
        fallback["certifications"] = []
        fallback["candidate_bio"]  = None
        fallback["_parse_error"]   = str(exc)
        return fallback


async def enrich_candidate(markdown: str, pre_extracted: dict) -> dict:
    """Backward-compatible alias for existing pipeline calls."""
    return await enrich(markdown, pre_extracted)
