from pydantic import BaseModel


class ScenarioRequest(BaseModel):
    scenario: str


class ScenarioResponse(BaseModel):
    scenario: str
    risk_score: float
    message: str