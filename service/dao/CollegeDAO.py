from service.models import College
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class CollegeDAO(BaseDAO):

    def apply_filters(self, q, params):
        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            q = q.filter(name__icontains=val)

        val = params.get("address", None)
        if DataValidator.isNotNull(val):
            q = q.filter(address__icontains=val)

        val = params.get("state", None)
        if DataValidator.isNotNull(val):
            q = q.filter(state=val)

        val = params.get("city", None)
        if DataValidator.isNotNull(val):
            q = q.filter(city__icontains=val)

        val = params.get("phoneNumber", None)
        if DataValidator.isNotNull(val):
            q = q.filter(phoneNumber__icontains=val)

        return q

    def get_model(self):
        return College
