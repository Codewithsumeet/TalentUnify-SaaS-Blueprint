from datetime import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String

from database import Base


class ShortlistRule(Base):
    __tablename__ = "shortlist_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    role_target = Column(String(200), nullable=True)
    min_score = Column(Integer, default=70)
    required_skills = Column(JSON, default=list)
    any_of_skills = Column(JSON, default=list)
    min_experience_years = Column(Float, default=0.0)
    location_filter = Column(String(100), nullable=True)
    level_filter = Column(JSON, default=list)
    auto_apply = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    match_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100), nullable=True)

