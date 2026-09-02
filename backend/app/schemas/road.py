from pydantic import BaseModel, ConfigDict
from typing import Optional


class RoadBase(BaseModel):
    name: str
    status: str = "OPEN"
    risk_score: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class RoadResponse(RoadBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoadStatusUpdate(BaseModel):
    status: str