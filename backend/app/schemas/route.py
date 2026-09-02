from pydantic import BaseModel
from typing import Optional


class RouteRequest(BaseModel):
    vehicle_id: Optional[int] = None
    origin: str
    destination: str


class RouteResponse(BaseModel):
    id: Optional[int] = None
    vehicle_id: Optional[int] = None
    origin: str
    destination: str
    status: str = "ACTIVE"
    distance_km: Optional[float] = None
    estimated_time_min: Optional[float] = None


class RerouteResponse(BaseModel):
    vehicle_id: int
    origin: str
    destination: str
    status: str
    message: str