from abc import ABC, abstractmethod
from services.db_service import DatabaseService

class BaseModel(ABC):
    def __init__(self):
        self.db = DatabaseService()

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @classmethod
    @abstractmethod
    def get_all(cls):
        pass

    @classmethod
    @abstractmethod
    def get_by_id(cls, id):
        pass