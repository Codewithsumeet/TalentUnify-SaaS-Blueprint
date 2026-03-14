from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class ScheduledInterview(Base):
    __tablename__ = "scheduled_interviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(
        UUID(as_uuid=True),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_type_uri = Column(String(500), nullable=True)
    calendly_link = Column(String(500), nullable=True)
    scheduling_link_uuid = Column(String(100), nullable=True, index=True)
    calendly_event_uri = Column(String(500), nullable=True)
    status = Column(String(20), default="link_created")
    scheduled_at = Column(DateTime, nullable=True)
    invitee_name = Column(String(200), nullable=True)
    invitee_email = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="interviews")

