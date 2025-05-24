from dataclasses import dataclass


@dataclass
class DroneDetectionInfoDTO:
    class_name: str
    class_conf: float
    class_bbox: list[float]

    model_name: str
    model_conf: float
    
    time_in_sec: float
