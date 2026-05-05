from service.models import User
from service.service.EmailBuilder import EmailBuilder
from service.service.EmailMessage import EmailMessage
from service.service.EmailService import EmailService
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

    def change_password(self, id, newPassword):
        try:
            user = self.get_model().objects.get(login=id)
        except self.get_model().DoesNotExist:
            return None

        user.password = newPassword
        user.save()

        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Password Changed Successfully"
        msg.text = EmailBuilder.change_password(
            {
                "firstName": user.firstName,
                "login": user.login,
                "password": newPassword,
            }
        )

        EmailService.send(msg)

        return user

    def forgot_password(self, login):
        try:
            user = self.get_model().objects.get(login=login)
            msg = EmailMessage()
            msg.to = [user.login]
            msg.subject = "Forgot Password Request"
            msg.text = EmailBuilder.forgot_password(
                {
                    "firstName": user.firstName,
                    "login": user.login,
                    "password": user.password,
                }
            )
            EmailService.send(msg)
            return user
        except self.get_model().DoesNotExist:
            return None

    def signup(self, user):
        self.save(user)
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Welcome - Registration Successful"
        msg.text = EmailBuilder.sign_up(
            {
                "firstName": user.firstName,
                "login": user.login,
                "password": user.password,
            }
        )
        EmailService.send(msg)
        return user

    def get_model(self):
        return User
