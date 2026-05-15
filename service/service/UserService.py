from service.dao.UserDAO import UserDAO
from service.mail.EmailBuilder import EmailBuilder
from service.mail.EmailMessage import EmailMessage
from service.mail.EmailService import EmailService
from .BaseService import BaseService


class UserService(BaseService):

    def authenticate(self, params):
        # Use exact login lookup then verify password — avoids icontains partial-match on login
        user = self._dao.get_by_login(params.get("loginId"))
        if user is not None and user.password == params.get("password"):
            return user
        return None

    def change_password(self, login, newPassword):
        user = self._dao.get_by_login(login)
        if user is None:
            return None
        user.password = newPassword
        user.save()
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Password Changed Successfully"
        msg.text = EmailBuilder.change_password({
            "firstName": user.firstName,
            "login": user.login,
            "password": newPassword,
        })
        EmailService.send(msg)
        return user

    def forgot_password(self, login):
        user = self._dao.get_by_login(login)
        if user is None:
            return None
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Forgot Password Request"
        msg.text = EmailBuilder.forgot_password({
            "firstName": user.firstName,
            "login": user.login,
            "password": user.password,
        })
        EmailService.send(msg)
        return user

    def signup(self, user):
        self.save(user)
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Welcome - Registration Successful"
        msg.text = EmailBuilder.sign_up({
            "firstName": user.firstName,
            "login": user.login,
            "password": user.password,
        })
        EmailService.send(msg)
        return user

    def get_dao(self):
        return UserDAO()
