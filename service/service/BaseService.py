import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseService(ABC):

    def __init__(self):
        self._dao = self.get_dao()

    def get(self, pk):
        return self._dao.get(pk)

    def search(self, params=None):
        return self._dao.search(params or {})

    def save(self, obj):
        return self._dao.save(obj)

    def delete(self, pk):
        return self._dao.delete(pk)

    def find_by_unique_key(self, pk):
        return self._dao.find_by_unique_key(pk)

    def get_model(self):
        return self._dao.get_model()

    @abstractmethod
    def get_dao(self):
        pass
