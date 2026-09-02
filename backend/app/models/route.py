from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, nullable=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    status = Column(String, nullable=False, default="ACTIVE")
    distance_km = Column(Float, nullable=True)
    estimated_time_min = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())