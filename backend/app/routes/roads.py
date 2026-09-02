from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.road import RoadSegment
from app.schemas.road import RoadResponse, RoadStatusUpdate


router = APIRouter(
    prefix="/roads",
    tags=["Roads"]
)


@router.get("/", response_model=list[RoadResponse])
def get_roads(db: Session = Depends(get_db)):
    return db.query(RoadSegment).all()


@router.get("/{road_id}", response_model=RoadResponse)
def get_road(road_id: int, db: Session = Depends(get_db)):
    road = db.query(RoadSegment).filter(
        RoadSegment.id == road_id
    ).first()

    if not road:
        raise HTTPException(
            status_code=404,
            detail="Road not found"
        )

    return road


@router.patch("/{road_id}/status", response_model=RoadResponse)
def update_road_status(
    road_id: int,
    data: RoadStatusUpdate,
    db: Session = Depends(get_db)
):
    road = db.query(RoadSegment).filter(
        RoadSegment.id == road_id
    ).first()

    if not road:
        raise HTTPException(
            status_code=404,
            detail="Road not found"
        )

    road.status = data.status
    db.commit()
    db.refresh(road)

    return road