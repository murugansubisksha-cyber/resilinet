from fastapi import APIRouter, HTTPException

from app.schemas.route import (
    RouteRequest,
    RouteResponse,
    RerouteResponse,
)


router = APIRouter(
    tags=["Routing"]
)


@router.post("/route", response_model=RouteResponse)
def create_route(data: RouteRequest):
    if not data.origin or not data.destination:
        raise HTTPException(
            status_code=400,
            detail="Origin and destination are required"
        )

    return {
        "vehicle_id": data.vehicle_id,
        "origin": data.origin,
        "destination": data.destination,
        "status": "ACTIVE",
        "distance_km": None,
        "estimated_time_min": None,
    }


@router.post(
    "/reroute/{vehicle_id}",
    response_model=RerouteResponse
)
def reroute_vehicle(vehicle_id: int):
    return {
        "vehicle_id": vehicle_id,
        "origin": "CURRENT_LOCATION",
        "destination": "DESTINATION",
        "status": "REROUTED",
        "message": "Vehicle rerouted successfully."
    }