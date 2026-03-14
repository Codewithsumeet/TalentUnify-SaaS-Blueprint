from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id                = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name              = Column(String(255),  nullable=True)
    email             = Column(String(255),  nullable=True, index=True, unique=False)
    phone             = Column(String(50),   nullable=True)
    location          = Column(String(255),  nullable=True)
    linkedin_url      = Column(String(500),  nullable=True)
    github_url        = Column(String(500),  nullable=True)
    current_role      = Column(String(255),  nullable=True)
    current_company   = Column(String(255),  nullable=True)
    experience_years  = Column(Float,        nullable=True)
    # Allowed values: Fresher | Junior | Mid | Senior | Principal
    experience_level  = Column(String(50),   nullable=True)
    skills            = Column(JSON,         default=list,  nullable=False)
    all_experience    = Column(JSON,         default=list,  nullable=False)
    certifications    = Column(JSON,         default=list,  nullable=False)
    candidate_bio     = Column(Text,         nullable=True)
    sources           = Column(JSON,         default=list,  nullable=False)
    github_enrichment = Column(JSON,         nullable=True)
    # high | medium | low — reflects which Tier 1 parser was used
    parse_quality     = Column(String(20),   default="high")
    # Which Pinecone index this candidate's vector lives in
    pinecone_index    = Column(String(50),   nullable=True)
    ai_score          = Column(Integer,       nullable=False, default=0)
    pipeline_stage    = Column(String(50),    nullable=False, default="applied")

    # ── Merge fields ──────────────────────────────────────────────────────────
    status             = Column(String(20),  nullable=False, default="active")
    merged_into        = Column(String(36),  nullable=True)
    merged_by          = Column(String(100), nullable=True)
    suggested_merge_id = Column(String(36),  nullable=True)

    # ── Fraud fields ──────────────────────────────────────────────────────────
    fraud_risk    = Column(String(10), nullable=False, default="low")
    fraud_score   = Column(Integer,    nullable=False, default=10)
    fraud_signals = Column(JSON,       nullable=False, default=list)

    # ── Shortlist fields ──────────────────────────────────────────────────────
    shortlisted       = Column(Boolean,    nullable=False, default=False)
    shortlist_rule_id = Column(String(36), nullable=True)

    created_at        = Column(DateTime,     default=datetime.utcnow)
    updated_at        = Column(DateTime,     default=datetime.utcnow, onupdate=datetime.utcnow)

    interviews = relationship(
        "ScheduledInterview",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )
    notes = relationship(
        "CandidateNote",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

    def to_dict(self) -> dict:
        """Serialize candidate for rule engine and async task processing."""
        ai_score = getattr(self, "ai_score", 0) or 0
        pipeline_stage = getattr(self, "pipeline_stage", None)
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "currentRole": self.current_role,
            "current_role": self.current_role,
            "aiScore": ai_score,
            "ai_score": ai_score,
            "experience_years": self.experience_years or 0,
            "experience_level": self.experience_level,
            "skills": self.skills or [],
            "location": self.location,
            "pipelineStage": pipeline_stage,
            "pipeline_stage": pipeline_stage,
            "shortlisted": self.shortlisted,
            "fraud_risk": self.fraud_risk,
            "fraud_score": self.fraud_score,
            "fraud_signals": self.fraud_signals or [],
            "all_experience": self.all_experience or [],
            "sources": self.sources or [],
            "suggested_merge_id": self.suggested_merge_id,
        }


from models.scheduled_interview import ScheduledInterview  # noqa: E402,F401
from models.candidate_note import CandidateNote  # noqa: E402,F401
