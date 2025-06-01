from .service import UpdateUserLocationService

from src.shared.api.mongo_db import MongoDBClient


class UpdateUserLocationServiceFactory:

    @staticmethod
    def create():
        return UpdateUserLocationService(
            MongoDBClient,
        )
