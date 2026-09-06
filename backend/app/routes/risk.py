import os
import sys

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


# Add the ML source directory to Python's path.
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
    )
)

ML_SRC = os.path.join(
    BASE_DIR,
    "ml",
    "src",
)

if ML_SRC not in sys.path:
    sys.path.insert(0, ML_SRC)


try:
    from predict import predict_risk

    ML_AVAILABLE = True

except Exception:
    predict_risk = None
    ML_AVAILABLE = False


def get_risk_level(risk_score: float) -> str:
    """Convert risk score into ResiliNet risk level."""

    risk_score = max(
        0.0,
        min(1.0, float(risk_score))
    )

    if risk_score <= 0.24:
        return "LOW"

    elif risk_score <= 0.49:
        return "MEDIUM"

    elif risk_score <= 0.74:
        return "HIGH"

    else:
        return "CRITICAL"


def rule_based_fallback(data: RiskPredictRequest):

    risk_score = 0.0

    if data.slope >= 25:
        risk_score += 0.35

    elif data.slope >= 15:
        risk_score += 0.20

    if data.elevation >= 430:
        risk_score += 0.20

    elif data.elevation >= 400:
        risk_score += 0.10

    if data.incident_count >= 5:
        risk_score += 0.30

    elif data.incident_count >= 3:
        risk_score += 0.20

    if data.road_importance >= 5:
        risk_score += 0.15

    elif data.road_importance >= 4:
        risk_score += 0.10

    risk_score = min(
        1.0,
        risk_score
    )

    factors = {
        "slope": (
            "CRITICAL"
            if data.slope >= 27
            else "HIGH"
            if data.slope >= 20
            else "MEDIUM"
            if data.slope >= 10
            else "LOW"
        ),
        "road_importance": (
            "CRITICAL"
            if data.road_importance >= 5
            else "HIGH"
            if data.road_importance >= 4
            else "MEDIUM"
            if data.road_importance >= 2
            else "LOW"
        ),
        "elevation": (
            "CRITICAL"
            if data.elevation >= 440
            else "HIGH"
            if data.elevation >= 410
            else "MEDIUM"
            if data.elevation >= 375
            else "LOW"
        ),
        "historical_incidents": (
            "CRITICAL"
            if data.incident_count >= 5
            else "HIGH"
            if data.incident_count >= 3
            else "MEDIUM"
            if data.incident_count >= 1
            else "LOW"
        ),
    }

    return {
        "road_id": data.road_id,
        "risk_score": round(
            risk_score,
            4
        ),
        "risk_level": get_risk_level(
            risk_score
        ),
        "factors": factors,
        "source": "RULE_BASED_FALLBACK",
    }


@router.post(
    "/predict",
    response_model=RiskPredictResponse
)
def predict_risk_endpoint(
    data: RiskPredictRequest
):

    if not ML_AVAILABLE:
        fallback = rule_based_fallback(data)

        return fallback

    try:

        ml_input = {
            "elevation": data.elevation,
            "slope": data.slope,
            "road_importance": data.road_importance,
            "incident_count": data.incident_count,
        }

        result = predict_risk(
            ml_input
        )

        return {
            "road_id": data.road_id,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "factors": result["factors"],
        }

    except Exception as error:

        print(
            f"ML prediction failed: {error}"
        )

        fallback = rule_based_fallback(data)

        return fallback


@road_risk_router.get(
    "/{road_id}/risk"
)
def get_road_risk(
    road_id: int
):

    if road_id <= 0:

        raise HTTPException(
            status_code=400,
            detail="Road ID must be greater than 0"
        )

    return {
        "road_id": road_id,
        "risk_score": 0.0,
        "risk_level": "LOW",
        "message": (
            "Road risk requires "
            "feature data for ML prediction."
        )
    }