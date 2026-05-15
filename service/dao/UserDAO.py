from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class UserDAO(BaseDAO):

    def apply_filters(self, q, params):
        val = params.get("firstName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(firstName__icontains=val)

        val = params.get("lastName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(lastName__icontains=val)

        val = params.get("login", None)
        if DataValidator.isNotNull(val):
            q = q.filter(login__icontains=val)

        val = params.get("password", None)
        if DataValidator.isNotNull(val):
            q = q.filter(password=val)

        val = params.get("mobileNumber", None)
        if DataValidator.isNotNull(val):
            q = q.filter(mobileNumber__icontains=val)

        val = params.get("gender", None)
        if DataValidator.isNotNull(val):
            q = q.filter(gender=val)

        val = params.get("role_id", None)
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(role_id=val)

        return q

    def get_by_login(self, login):
        try:
            return self.get_model().objects.get(login=login)
        except self.get_model().DoesNotExist:
            return None

    def get_model(self):
        return User
