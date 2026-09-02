from pydantic import BaseModel, ConfigDict
from typing import Optional


class VehicleBase(BaseModel):
    vehicle_number: str
    vehicle_type: str
    priority: int = 1
    status: str = "ACTIVE"
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class VehicleCreate(VehicleBase):
    pass


class VehicleResponse(VehicleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class VehicleUpdate(BaseModel):
    vehicle_type: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None