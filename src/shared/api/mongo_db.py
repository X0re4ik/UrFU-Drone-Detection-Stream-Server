from pymongo import MongoClient
from contextlib import contextmanager

from src.shared.configs import PROJECT_SETTINGS


class MongoManager:
    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    @contextmanager
    def get_collection(self, collection_name: str):
        """Контекстный менеджер для работы с коллекцией MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            collection = self.db[collection_name]
            yield collection  # Передаем коллекцию в контекст
        finally:
            # Закрываем соединение с MongoDB, когда контекст завершен
            if self.client:
                self.client.close()


MongoDBClient = MongoManager(PROJECT_SETTINGS.mongo_db.URI, "DroneDetection")
