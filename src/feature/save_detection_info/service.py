from src.shared.api.mongo_db import MongoDBClient, MongoManager

from .dto import DroneDetectionInfoDTO


from src.shared.api.logger import Logger


logger = Logger


class DetectionSaver:

    def __init__(self, mongo_manager: MongoManager):
        self._mongo_manager = mongo_manager

        self._buffer: list[DroneDetectionInfoDTO] = []

        self._buffer_size = 10
        self._buffer_point = 0

    def save(self, drone_detection: DroneDetectionInfoDTO) -> None:

        self._buffer.append(drone_detection)
        self._buffer_point += 1
        if self._buffer_point < self._buffer_size:
            logger.info(self._buffer_point, self._buffer_size)
            return

        logger.info(f"Write To MongoDB Statistics (size={len(self._buffer)})")

        with self._mongo_manager.get_collection("DetectionResult") as collection:

            collection.insert_many(
                [
                    {
                        "timestamp": drone_detection.timestamp,
                        "modelType": drone_detection.model_type,
                        "modelConf": drone_detection.model_conf,
                        "bbox": drone_detection.bbox,
                    }
                    for drone_detection in self._buffer
                ]
            )

        self._buffer_point = 0
        self._buffer.clear()
