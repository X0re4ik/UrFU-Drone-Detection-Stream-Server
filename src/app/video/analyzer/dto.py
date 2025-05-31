from pydantic import BaseModel


class DroneDetectionVideoInfoDTO(BaseModel):
    count_drones: int
    model_types: list[str]
