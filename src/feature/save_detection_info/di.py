from .service import DetectionSaver

from src.shared.api.mongo_db import MongoDBClient


class DetectionSaverFactory:

    @staticmethod
    def create():
        return DetectionSaver(
            MongoDBClient,
        )
