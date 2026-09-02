from fastapi import APIRouter, Query


router = APIRouter(
    prefix="/accessibility",
    tags=["Accessibility"]
)


@router.get("/")
def get_accessibility(
    road_id: int | None = Query(default=None)
):
    return {
        "road_id": road_id,
        "accessible": True,
        "message": "Accessibility information is currently available."
    }