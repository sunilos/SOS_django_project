from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class ForgetPasswordDAO(BaseDAO):

    def apply_filters(self, q, params):
        val = params.get("login", None)
        if DataValidator.isNotNull(val):
            q = q.filter(login=val)

        return q

    def get_model(self):
        return User
