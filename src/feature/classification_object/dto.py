from dataclasses import dataclass



@dataclass
class ClassificationInfoDTO:
    confidence: float
    model_id: int
