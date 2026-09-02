from fastapi import APIRouter

from app.schemas.sync import (
    SyncIncidentsRequest,
    SyncIncidentsResponse,
    SyncIncidentResult,
)


router = APIRouter(
    prefix="/sync",
    tags=["Offline Sync"]
)


@router.post(
    "/incidents",
    response_model=SyncIncidentsResponse
)
def sync_incidents(data: SyncIncidentsRequest):
    results = []

    for incident in data.incidents:
        results.append(
            SyncIncidentResult(
                client_id=incident.client_id,
                incident_id=None,
                status="RECEIVED",
            )
        )

    return SyncIncidentsResponse(results=results)