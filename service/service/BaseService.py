import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseService(ABC):

    def __init__(self):
        self._dao = self.get_dao()

    def get(self, pk):
        return self._dao.get(pk)

    def search(self, params=None, page_number=1, page_size=10):
        # Normalise early so all code below can safely use params as a dict
        params = params or {}
        result = self._dao.search(params, page_number, page_size)

        # page_number == 0 returns a plain QuerySet — no Page attributes available
        if page_number == 0:
            return result
        
        params["has_next"] = result.has_next()
        params["has_previous"] = result.has_previous()
        params["start_index"] = (page_number - 1) * page_size
        params["end_index"] = params["start_index"] + len(result.object_list)
        
        return result

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
