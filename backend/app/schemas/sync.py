from pydantic import BaseModel
from typing import List, Optional


class SyncIncident(BaseModel):
    client_id: str
    type: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    road_id: Optional[int] = None
    reported_by: Optional[int] = None


class SyncIncidentsRequest(BaseModel):
    incidents: List[SyncIncident]


class SyncIncidentResult(BaseModel):
    client_id: str
    incident_id: Optional[int] = None
    status: str


class SyncIncidentsResponse(BaseModel):
    results: List[SyncIncidentResult]