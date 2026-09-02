from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from app.database import Base


class RoadEvent(Base):
    __tablename__ = "road_events"

    id = Column(Integer, primary_key=True, index=True)
    road_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())