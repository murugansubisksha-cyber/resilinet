from fastapi import APIRouter, HTTPException

from app.schemas.scenario import (
    ScenarioRequest,
    ScenarioResponse,
)


router = APIRouter(
    prefix="/scenario",
    tags=["Scenarios"]
)


SCENARIO_RISK = {
    "normal": 0.86,
    "heavy-rain": 0.61,
    "landslide": 0.34,
    "flood": 0.34,
    "restore": 0.71,
}


@router.post(
    "/{scenario_name}",
    response_model=ScenarioResponse
)
def run_scenario(
    scenario_name: str,
    data: ScenarioRequest
):
    scenario = scenario_name.lower()

    if scenario not in SCENARIO_RISK:
        raise HTTPException(
            status_code=400,
            detail="Unknown scenario"
        )

    if data.scenario.lower() != scenario:
        raise HTTPException(
            status_code=400,
            detail="Scenario name does not match request"
        )

    return {
        "scenario": scenario,
        "risk_score": SCENARIO_RISK[scenario],
        "message": f"{scenario} scenario applied successfully."
    }