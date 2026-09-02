from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.incident import Incident
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.get("/", response_model=list[IncidentResponse])
def get_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()


@router.post("/", response_model=IncidentResponse)
def create_incident(
    data: IncidentCreate,
    db: Session = Depends(get_db)
):
    incident = Incident(
        type=data.type,
        description=data.description,
        status="REPORTED",
        latitude=data.latitude,
        longitude=data.longitude,
        road_id=data.road_id,
        reported_by=data.reported_by,
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    data: IncidentUpdate,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(incident, field, value)

    db.commit()
    db.refresh(incident)

    return incident