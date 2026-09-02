from pydantic import BaseModel
from typing import Optional


class VerificationRequest(BaseModel):
    incident_id: int
    verified: bool
    confidence: Optional[float] = None


class VerificationResponse(BaseModel):
    incident_id: int
    status: str
    message: str