from fastapi import APIRouter

from app.models.weather import Weather


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


@router.get("/")
def get_weather():
    return {
        "location": "ResiliNet Area",
        "condition": "CLEAR",
        "temperature": None,
        "rainfall": None,
        "wind_speed": None,
        "message": "Weather data endpoint is ready."
    }