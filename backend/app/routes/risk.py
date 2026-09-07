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


try:
    from ml.src.risk_service import predict_risk

    ML_AVAILABLE = True

except Exception as error:

    print(
        f"ML service import failed: {error}"
    )

    predict_risk = None
    ML_AVAILABLE = False


def get_risk_level(
    risk_score: float
) -> str:

    """
    Convert risk score into ResiliNet risk level.
    """

    risk_score = max(
        0.0,
        min(
            1.0,
            float(risk_score)
        )
    )

    if risk_score <= 0.24:
        return "LOW"

    elif risk_score <= 0.49:
        return "MEDIUM"

    elif risk_score <= 0.74:
        return "HIGH"

    else:
        return "CRITICAL"


def rule_based_fallback(
    data: RiskPredictRequest
):

    """
    Rule-based fallback used only when
    the ML service is unavailable.
    """

    risk_score = 0.0

    if data.weather_severity_index >= 0.80:
        risk_score += 0.30

    elif data.weather_severity_index >= 0.60:
        risk_score += 0.20

    elif data.weather_severity_index >= 0.30:
        risk_score += 0.10

    if data.rainfall >= 250:
        risk_score += 0.20

    elif data.rainfall >= 150:
        risk_score += 0.12

    elif data.rainfall >= 50:
        risk_score += 0.05

    if data.slope >= 25:
        risk_score += 0.20

    elif data.slope >= 15:
        risk_score += 0.12

    if data.elevation >= 430:
        risk_score += 0.10

    elif data.elevation >= 400:
        risk_score += 0.05

    if data.incident_count >= 5:
        risk_score += 0.20

    elif data.incident_count >= 3:
        risk_score += 0.12

    elif data.incident_count >= 1:
        risk_score += 0.05

    if data.road_importance >= 5:
        risk_score += 0.10

    elif data.road_importance >= 4:
        risk_score += 0.05

    risk_score = min(
        1.0,
        risk_score
    )

    factors = {
        "rainfall": (
            "CRITICAL"
            if data.rainfall >= 250
            else "HIGH"
            if data.rainfall >= 150
            else "MEDIUM"
            if data.rainfall >= 50
            else "LOW"
        ),

        "weather_severity": (
            "CRITICAL"
            if data.weather_severity_index >= 0.80
            else "HIGH"
            if data.weather_severity_index >= 0.60
            else "MEDIUM"
            if data.weather_severity_index >= 0.30
            else "LOW"
        ),

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

    """
    Predict road risk using the trained XGBoost model.
    """

    if not ML_AVAILABLE:

        print(
            "ML service is unavailable."
        )

        print(
            "Using rule-based fallback."
        )

        return rule_based_fallback(
            data
        )

    ml_input = {
        "rainfall": data.rainfall,

        "accumulated_rainfall_24h":
            data.accumulated_rainfall_24h,

        "accumulated_rainfall_72h":
            data.accumulated_rainfall_72h,

        "rainfall_intensity":
            data.rainfall_intensity,

        "weather_severity_index":
            data.weather_severity_index,

        "elevation":
            data.elevation,

        "slope":
            data.slope,

        "road_importance":
            data.road_importance,

        "incident_count":
            data.incident_count,
    }

    try:

        print(
            "Calling ML risk service..."
        )

        print(
            f"ML input: {ml_input}"
        )

        result = predict_risk(
            ml_input
        )

        print(
            f"ML result: {result}"
        )

        print(
            "ML prediction successful."
        )

        return {
            "road_id": data.road_id,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "factors": result.get(
                "factors",
                {}
            ),
            "source": "XGBOOST",
        }

    except Exception as error:

        print(
            f"ML prediction failed: {error}"
        )

        print(
            "Using rule-based fallback."
        )

        return rule_based_fallback(
            data
        )


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
            "feature data for ML prediction. "
            "Use POST /risk/predict."
        )
    }