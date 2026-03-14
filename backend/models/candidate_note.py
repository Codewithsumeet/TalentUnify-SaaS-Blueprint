from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class CandidateNote(Base):
    __tablename__ = "candidate_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    text = Column(Text, nullable=False)
    author = Column(String(120), nullable=False, default="Recruiter")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="notes")
