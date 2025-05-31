from pydantic import BaseModel

class DroneTypeInfoDTO(BaseModel):
    model_name: str
    maximum_payload: float
    maximum_speed: float
    cruising_speed: float
    communication_range: float
    photo: bytes
