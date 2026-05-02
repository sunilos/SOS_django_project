import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """Abstract base class for all service classes.

    Provides common CRUD operations (get, search, save, delete)
    backed by a Django ORM model returned by get_model().
    Subclasses must implement get_model() and may override search()
    to apply query filters.
    """

    def __init__(self):
        pass

    def get(self, pk):
        """Return the model instance with the given primary key, or None if not found."""
        try:
            obj = self.get_model().objects.get(id=pk)
            logger.debug("%s.get() pk=%s found", self.__class__.__name__, pk)
            return obj
        except self.get_model().DoesNotExist:
            logger.warning("%s.get() pk=%s not found", self.__class__.__name__, pk)
            return None

    def search(self):
        """Return all model instances, or None if the table is empty."""
        try:
            records = self.get_model().objects.all()
            logger.debug("%s.search() returned %s records", self.__class__.__name__, records.count())
            return records
        except self.get_model().DoesNotExist:
            logger.warning("%s.search() no records found", self.__class__.__name__)
            return None

    def save(self, obj):
        """Insert a new record or update an existing one.

        An id of 0 is treated as a new record (id set to None so the
        database auto-assigns the primary key).
        """
        is_new = obj.id == 0
        if is_new:
            obj.id = None
        obj.save()
        logger.info("%s.save() %s pk=%s", self.__class__.__name__, "inserted" if is_new else "updated", obj.id)

    def delete(self, pk):
        """Delete the model instance with the given primary key."""
        obj = self.get(pk)
        obj.delete()
        logger.info("%s.delete() pk=%s deleted", self.__class__.__name__, pk)

    def find_by_unique_key(self, pk):
        """Return the model instance matching the given unique key, or None if not found."""
        try:
            obj = self.get_model().objects.get(id=pk)
            logger.debug("%s.find_by_unique_key() pk=%s found", self.__class__.__name__, pk)
            return obj
        except self.get_model().DoesNotExist:
            logger.warning("%s.find_by_unique_key() pk=%s not found", self.__class__.__name__, pk)
            return None

    @abstractmethod
    def get_model(self):
        """Return the Django model class this service operates on."""
        pass
