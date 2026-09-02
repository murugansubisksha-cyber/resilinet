from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="REPORTED")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    road_id = Column(Integer, nullable=True)
    reported_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())