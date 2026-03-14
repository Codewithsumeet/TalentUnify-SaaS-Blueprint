"""
HRMS Mock Integration.

Simulates an HRMS (e.g., Workday, BambooHR) pushing candidate data to TalentFlow.
In production, this would be a real OAuth-secured HRMS webhook.
For the hackathon, it provides a /api/v1/intake/hrms-push endpoint that accepts
structured JSON and feeds it into the same Celery pipeline as file uploads.

This makes the "HRMS" intake source light up on the dashboard.
"""
import json
import uuid
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/intake")


class HRMSCandidate(BaseModel):
    """Structured candidate data as an HRMS would provide it."""
    name:             str
    email:            Optional[str]  = None
    phone:            Optional[str]  = None
    location:         Optional[str]  = None
    current_role:     Optional[str]  = None
    current_company:  Optional[str]  = None
    experience_years: Optional[float] = None
    skills:           list[str]      = []
    resume_text:      Optional[str]  = None
    linkedin_url:     Optional[str]  = None
    source_system:    str            = "hrms_mock"


class HRMSBatchPayload(BaseModel):
    candidates: list[HRMSCandidate]
    batch_id:   Optional[str] = None


def _candidate_to_markdown(c: HRMSCandidate) -> str:
    """Convert structured HRMS record to markdown so it flows through the same pipeline."""
    lines = [
        f"# {c.name}",
        "",
        f"**Current Role:** {c.current_role or 'N/A'}",
        f"**Current Company:** {c.current_company or 'N/A'}",
        f"**Email:** {c.email or 'N/A'}",
        f"**Phone:** {c.phone or 'N/A'}",
        f"**Location:** {c.location or 'N/A'}",
        f"**LinkedIn:** {c.linkedin_url or 'N/A'}",
        f"**Years of Experience:** {c.experience_years or 0}",
        "",
        "## Skills",
        ", ".join(c.skills) if c.skills else "N/A",
    ]
    if c.resume_text:
        lines += ["", "## Resume", c.resume_text]
    return "\n".join(lines)


@router.post("/hrms-push")
async def hrms_push(payload: HRMSBatchPayload):
    """
    Accepts a batch of HRMS candidate records and queues each for processing.
    The markdown conversion ensures HRMS candidates flow through the same
    enrichment pipeline as uploaded PDFs.
    """
    task_ids = []
    batch_id = payload.batch_id or str(uuid.uuid4())[:8]
    from tasks.resume_tasks import parse_resume

    for candidate in payload.candidates:
        markdown  = _candidate_to_markdown(candidate)
        # Encode as UTF-8 bytes — the pipeline expects bytes from extractor
        md_bytes  = markdown.encode("utf-8")

        task = parse_resume.delay(
            file_bytes = md_bytes,
            mime_type  = "text/markdown",   # pipeline detects this and skips LlamaParse
            source     = "hrms",
            filename   = f"{candidate.name.replace(' ', '_')}_hrms.md",
            metadata   = {
                "source_system": candidate.source_system,
                "batch_id":      batch_id,
                "pre_extracted": {
                    "name":             candidate.name,
                    "email":            candidate.email,
                    "phone":            candidate.phone,
                    "location":         candidate.location,
                    "current_role":     candidate.current_role,
                    "current_company":  candidate.current_company,
                    "experience_years": candidate.experience_years,
                    "skills_phase2":    candidate.skills,
                    "linkedin_url":     candidate.linkedin_url,
                },
            },
        )
        task_ids.append({"name": candidate.name, "task_id": task.id})

    return {
        "batch_id":    batch_id,
        "queued":      len(task_ids),
        "tasks":       task_ids,
        "status":      "queued",
    }


@router.post("/hrms-demo")
async def hrms_demo():
    """
    Seeds the database with 5 realistic fintech candidates for demo day.
    Call once: POST /api/v1/intake/hrms-demo
    """
    demo_candidates = [
        HRMSCandidate(
            name="Ananya Shah", email="ananya.shah@example.com",
            location="Bangalore", current_role="Senior Backend Engineer",
            current_company="PhonePe", experience_years=6.0,
            skills=["Go", "Kafka", "PostgreSQL", "Redis", "Docker", "Kubernetes"],
            source_system="hrms_mock"
        ),
        HRMSCandidate(
            name="Rohan Verma", email="rohan.verma@example.com",
            location="Mumbai", current_role="ML Engineer",
            current_company="Razorpay", experience_years=4.5,
            skills=["Python", "PyTorch", "LangChain", "FastAPI", "Pinecone"],
            source_system="hrms_mock"
        ),
        HRMSCandidate(
            name="Priya Nair", email="priya.nair@example.com",
            location="Hyderabad", current_role="Full Stack Engineer",
            current_company="Paytm", experience_years=3.0,
            skills=["React", "Node.js", "TypeScript", "MongoDB", "AWS"],
            source_system="hrms_mock"
        ),
        HRMSCandidate(
            name="Karan Mehta", email="karan.mehta@example.com",
            location="Pune", current_role="Blockchain Developer",
            current_company="Polygon", experience_years=5.0,
            skills=["Solidity", "Web3", "Rust", "Go", "DeFi"],
            source_system="hrms_mock"
        ),
        HRMSCandidate(
            name="Divya Krishnan", email="divya.krishnan@example.com",
            location="Chennai", current_role="Data Engineer",
            current_company="CRED", experience_years=2.5,
            skills=["Python", "Apache Spark", "Apache Kafka", "PostgreSQL", "Airflow"],
            source_system="hrms_mock"
        ),
    ]
    return await hrms_push(HRMSBatchPayload(candidates=demo_candidates, batch_id="demo-seed"))
