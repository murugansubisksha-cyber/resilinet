from pydantic import BaseModel, Field


class RiskPredictRequest(BaseModel):

    road_id: int

    rainfall: float = Field(..., ge=0)

    accumulated_rainfall_24h: float = Field(..., ge=0)

    accumulated_rainfall_72h: float = Field(..., ge=0)

    rainfall_intensity: float = Field(..., ge=0)

    weather_severity_index: float = Field(
        ...,
        ge=0,
        le=1
    )

    elevation: float = Field(..., ge=0)

    slope: float = Field(
        ...,
        ge=0,
        le=30
    )

    road_importance: float = Field(
        ...,
        ge=1,
        le=5
    )

    incident_count: float = Field(
        ...,
        ge=0
    )


class RiskPredictResponse(BaseModel):

    road_id: int

    risk_score: float

    risk_level: str

    factors: dict[str, str]

    source: str