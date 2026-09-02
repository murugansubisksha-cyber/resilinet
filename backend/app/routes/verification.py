from fastapi import APIRouter, HTTPException

from app.schemas.verification import (
    VerificationRequest,
    VerificationResponse,
)


router = APIRouter(
    prefix="/verify",
    tags=["Verification"]
)


@router.post(
    "/{incident_id}",
    response_model=VerificationResponse
)
def verify_incident(
    incident_id: int,
    data: VerificationRequest
):
    if data.incident_id != incident_id:
        raise HTTPException(
            status_code=400,
            detail="Incident ID does not match request"
        )

    if data.verified:
        status = "VERIFIED"
        message = "Incident verified successfully."
    else:
        status = "REJECTED"
        message = "Incident rejected."

    return {
        "incident_id": incident_id,
        "status": status,
        "message": message,
    }