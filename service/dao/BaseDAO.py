import logging
from abc import ABC, abstractmethod

from django.db.models import CharField, TextField, IntegerField

from service.utility.DataValidator import DataValidator

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

    def search(self, params):
        model = self.get_model()
        field_map = {f.name: f for f in model._meta.get_fields() if hasattr(f, "column")}
        q = model.objects.filter()

        for key, val in params.items():
            if not DataValidator.isNotNull(val):
                continue
            field = field_map.get(key)
            if field is None:
                continue
            # IntegerField whose name ends with _id/_ID is a reference ID — skip sentinel "0"
            if isinstance(field, IntegerField) and field.name.lower().endswith("_id") and str(val) == "0":
                continue
            if isinstance(field, (CharField, TextField)):
                q = q.filter(**{f"{key}__icontains": val})
            else:
                q = q.filter(**{key: val})

        return q

    @abstractmethod
    def get_model(self):
        pass
