import uuid

from sqlalchemy import Column, DateTime, String, Text, UniqueConstraint

from database import Base


class IntegrationToken(Base):
    __tablename__ = "integration_tokens"
    __table_args__ = (UniqueConstraint("service", name="uq_integration_tokens_service"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    service = Column(String(50), nullable=False, index=True)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)

