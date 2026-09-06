from pydantic import BaseModel, Field


class RiskPredictRequest(BaseModel):
    road_id: int
    elevation: float = Field(..., ge=0)
    slope: float = Field(..., ge=0, le=30)
    road_importance: float = Field(..., ge=1, le=5)
    incident_count: float = Field(..., ge=0)


class RiskPredictResponse(BaseModel):
    road_id: int
    risk_score: float
    risk_level: str
    factors: dict[str, str]