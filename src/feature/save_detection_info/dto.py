from pydantic import BaseModel
from datetime import datetime


class DroneDetectionInfoDTO(BaseModel):
    model_type: str
    model_conf: float
    bbox: list[float]
    timestamp: datetime
