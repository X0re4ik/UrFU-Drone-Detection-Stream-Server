from src.shared.api.mongo_db import MongoDBClient, MongoManager

from .dto import DroneDetectionInfoDTO


from src.shared.api.logger import Logger


logger = Logger


class DetectionSaver:

    def __init__(self, mongo_manager: MongoManager):
        self._mongo_manager = mongo_manager

        self._buffer: list[DroneDetectionInfoDTO] = []

        self._buffer_size = 100
        self._buffer_point = 0

    def save(self, drone_detection: DroneDetectionInfoDTO) -> None:

        self._buffer.append(drone_detection)
        self._buffer_point += 1
        if self._buffer_point < self._buffer_size:
            return

        logger.info(f"Write To MongoDB Statistics (size={len(self._buffer)})")

        with self._mongo_manager.get_collection("DetectionInfo") as collection:

            collection.insert_many(
                [
                    {
                        "timeInSec": drone_detection.time_in_sec,
                        "className": drone_detection.class_name,
                        "classConf": drone_detection.class_conf,
                        "classBbox": drone_detection.class_bbox,
                        "modelName": drone_detection.model_name,
                        "modelConf": drone_detection.model_conf,
                    }
                    for drone_detection in self._buffer
                ]
            )

        self._buffer_point = 0
        self._buffer.clear()
