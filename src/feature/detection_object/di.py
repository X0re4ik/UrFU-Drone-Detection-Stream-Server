from ultralytics import YOLO
from .service import DetectionObjects


class DetectionObjectsFactory:

    def create(model: YOLO, tracker_path: str) -> DetectionObjects:
        return DetectionObjects(model, tracker_path)
