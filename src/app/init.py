import torch
from ultralytics import YOLO
from src.shared.configs import (
    YOLO_DETECTION_PATH,
    MOBILE_NET_CLASSIFICATION_PATH,
    TRACKER_PATH,
    PROJECT_SETTINGS,
)
from src.feature.detection_object import DetectionObjectsFactory, DetectionObjects
from src.feature.classification_object import (
    ClassificationObjectFactory,
    ClassificationObject,
)


__yolo_model = YOLO(YOLO_DETECTION_PATH).to(PROJECT_SETTINGS.app.device)

__mobile_net_model = torch.load(
    MOBILE_NET_CLASSIFICATION_PATH,
    map_location=PROJECT_SETTINGS.app.device,
)
__mobile_net_model.eval()

detection_service: DetectionObjects = DetectionObjectsFactory.create(
    __yolo_model, str(TRACKER_PATH)
)

classification_service: ClassificationObject = ClassificationObjectFactory.create(
    __mobile_net_model
)


CLASS_MAPPER: dict[int, str] = {
    0: "БПЛА",
    1: "Квадракоптер",
    2: "Птица",
    3: "Самолёт",
}

MODEL_MAPPER: dict[int, str] = {
    0: "A22 Foxbat",
    1: "Bayraktar TB2",
    2: "UJ-22 Airborne",
}
