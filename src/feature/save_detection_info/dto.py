from dataclasses import dataclass


@dataclass
class DroneDetectionInfoDTO:
    class_name: str
    class_conf: float
    model_conf: float
    bbox: list[float]
