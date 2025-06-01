from pydantic import BaseModel


class DroneDetectionResultDTO(BaseModel):
    drone_type: str
    drone_confidence: float
    type_confidence: float
    bbox: list[float]
