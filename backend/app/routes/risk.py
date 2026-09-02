from fastapi import APIRouter, HTTPException

from app.schemas.risk import (
    RiskPredictRequest,
    RiskPredictResponse,
)


router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)

road_risk_router = APIRouter(
    prefix="/roads",
    tags=["Risk"]
)


def calculate_risk_score(
    rainfall: float | None = None,
    weather_condition: str | None = None
) -> float:
    """Calculate a temporary risk score."""

    risk_score = 0.0

    if rainfall is not None:
        if rainfall > 50:
            risk_score = 0.8
        elif rainfall > 20:
            risk_score = 0.5

    if weather_condition:
        condition = weather_condition.lower()

        if condition in ["landslide", "flood"]:
            risk_score = max(risk_score, 0.9)
        elif condition in ["heavy-rain", "heavy rain"]:
            risk_score = max(risk_score, 0.7)

    return risk_score


def get_risk_level(risk_score: float) -> str:
    """Convert risk score into a risk level."""

    if risk_score >= 0.7:
        return "HIGH"
    elif risk_score >= 0.4:
        return "MEDIUM"
    else:
        return "LOW"


@router.post(
    "/predict",
    response_model=RiskPredictResponse
)
def predict_risk(data: RiskPredictRequest):

    risk_score = calculate_risk_score(
        rainfall=data.rainfall,
        weather_condition=data.weather_condition
    )

    risk_level = get_risk_level(risk_score)

    return {
        "road_id": data.road_id,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }


@road_risk_router.get("/{road_id}/risk")
def get_road_risk(road_id: int):

    if road_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Road ID must be greater than 0"
        )

    # Temporary value until database and ML model
    # are connected.
    risk_score = 0.0
    risk_level = get_risk_level(risk_score)

    return {
        "road_id": road_id,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "message": "Road risk endpoint is ready."
    }