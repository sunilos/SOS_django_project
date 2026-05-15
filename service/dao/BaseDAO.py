import logging
from abc import ABC, abstractmethod

from django.core.paginator import Paginator

logger = logging.getLogger(__name__)


class BaseDAO(ABC):

    def get(self, pk):
        try:
            return self.get_model().objects.get(id=pk)
        except self.get_model().DoesNotExist:
            logger.warning("%s.get() pk=%s not found", self.__class__.__name__, pk)
            return None

    def get_all(self):
        return self.get_model().objects.all()

    def save(self, obj):
        is_new = obj.id == 0
        if is_new:
            obj.id = None
        obj.save()
        logger.info("%s.save() %s pk=%s", self.__class__.__name__, "inserted" if is_new else "updated", obj.id)

    def delete(self, pk):
        obj = self.get(pk)
        if obj:
            obj.delete()
            logger.info("%s.delete() pk=%s deleted", self.__class__.__name__, pk)

    def find_by_unique_key(self, pk):
        return self.get(pk)
    
    def apply_filters(self, q, params):
        pass

    def search(self, params, page_number=1, page_size=10):
        """
        Search records with subclass-defined filters and optional pagination.

        Args:
            params      : dict of filter criteria passed to apply_filters()
            page_number : page to return (1-based); pass 0 to get all records
            page_size   : number of records per page (default 10)

        Returns:
            Page object when page_number > 0, QuerySet when page_number == 0
        """
        # Start with all records for this model
        q = self.get_model().objects.filter()

        # Delegate field-level filtering to the subclass
        q = self.apply_filters(q, params)

        # page_number == 0 means return all records without pagination
        if page_number == 0:
            return q

        # Apply pagination and return the requested page
        paginator = Paginator(q, page_size)
        return paginator.get_page(page_number)

    @abstractmethod
    def get_model(self):
        pass
