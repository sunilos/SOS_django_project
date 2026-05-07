from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class ForgetPasswordDAO(BaseDAO):

    def search(self, params):
        q = self.get_model().objects.filter()

        val = params.get("login", None)
        if DataValidator.isNotNull(val):
            q = q.filter(login=val)

        return q

    def get_model(self):
        return User
