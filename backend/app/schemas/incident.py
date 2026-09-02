from pydantic import BaseModel
from typing import Optional


class IncidentBase(BaseModel):
    type: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    road_id: Optional[int] = None
    reported_by: Optional[int] = None


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None


class IncidentResponse(IncidentBase):
    id: int
    status: str