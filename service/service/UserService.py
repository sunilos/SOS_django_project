from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

"""
It contains User business logics.   
"""


class UserService(BaseService):

    def authenticate(self, params):
        userList = self.search(params)
        if userList.count() > 0:
            print("8888888->", userList[0].login)
            return userList[0]
        else:
            return None

    def search(self, params):
        q = self.get_model().objects.filter()

        val = params.get("firstName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(firstName__icontains=val)

        val = params.get("lastName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(lastName__icontains=val)

        val = params.get("login", None)
        if DataValidator.isNotNull(val):
            q = q.filter(login=val)

        val = params.get("password", None)
        if DataValidator.isNotNull(val):
            q = q.filter(password=val)

        val = params.get("mobileNumber", None)
        if DataValidator.isNotNull(val):
            q = q.filter(mobileNumber=val)

        val = params.get("gender", None)
        if DataValidator.isNotNull(val):
            q = q.filter(gender=val)

        val = params.get("role_id", None)
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(role_id=val)

        return q

    def get_model(self):
        return User
