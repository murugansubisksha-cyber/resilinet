from fastapi import APIRouter

from app.schemas.risk import RiskPredictRequest, RiskPredictResponse


router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)


@router.post("/predict", response_model=RiskPredictResponse)
def predict_risk(data: RiskPredictRequest):
    # Temporary backend placeholder.
    # Person 4's ML model will be connected here later.
    risk_score = 0.0

    if data.rainfall is not None and data.rainfall > 50:
        risk_score = 0.8
    elif data.rainfall is not None and data.rainfall > 20:
        risk_score = 0.5

    if risk_score >= 0.7:
        risk_level = "HIGH"
    elif risk_score >= 0.4:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "road_id": data.road_id,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }