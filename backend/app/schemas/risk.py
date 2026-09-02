from pydantic import BaseModel
from typing import Optional


class RiskPredictRequest(BaseModel):
    road_id: int
    rainfall: Optional[float] = None
    weather_condition: Optional[str] = None


class RiskPredictResponse(BaseModel):
    road_id: int
    risk_score: float
    risk_level: str