from datetime import datetime

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import User
from service.Serializers import UserSerializers
from service.service.UserService import UserService
from service.service.ForgetPasswordService import ForgetPasswordService
from service.mail.EmailService import EmailService
from service.mail.EmailBuilder import EmailBuilder
from service.mail.EmailMessage import EmailMessage


class UserCtl(BaseRestCtl):
    def get_model(self):
        return User

    def get_serializer_class(self):
        return UserSerializers


class UserLoginCtl(BaseRestCtl):
    """
    REST endpoint for user authentication.

    POST /ORSAPI/api/User/login/

    Request body:
        {
            "login": "user@example.com",
            "password": "yourpassword"
        }

    Responses:
        200 - Valid credentials   : {"error": false, "message": "Login successful", "data": {"user": {...}, "access": "...", "refresh": "..."}}
        400 - Missing fields      : {"error": true,  "message": "Login and password are required"}
        401 - Wrong credentials   : {"error": true,  "message": "Invalid login or password"}
    """

    permission_classes = [AllowAny]

    def get_model(self):
        return User

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        login = request.data.get("login", "")
        password = request.data.get("password", "")

        if not login or not password:
            return self.error_response(None, "Login and password are required", status.HTTP_400_BAD_REQUEST)

        user = UserService().authenticate({"login": login, "password": password})
        if user is None:
            return self.error_response(None, "Invalid login or password", status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken()
        refresh["user_id"] = user.id
        refresh["login"] = user.login
        refresh["role_id"] = user.role_id

        return Response({
            "error": False,
            "message": "Login successful",
            "data": {
                "user": UserSerializers(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        })


class ChangePasswordCtl(BaseRestCtl):
    """
    REST endpoint to change a user's password.

    POST /ORSAPI/api/User/change-password/

    Request body:
        {
            "login": "user@example.com",
            "oldPassword": "current",
            "newPassword": "newpass",
            "confirmPassword": "newpass"
        }

    Responses:
        200 - Success      : {"error": false, "message": "Password changed successfully"}
        400 - Validation   : {"error": true,  "message": "...", "errors": {...}}
        404 - User missing : {"error": true,  "message": "User not found"}
    """

    def get_model(self):
        return User

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        login = request.data.get("login", "")
        old_password = request.data.get("oldPassword", "")
        new_password = request.data.get("newPassword", "")
        confirm_password = request.data.get("confirmPassword", "")

        errors = {}
        if not login:
            errors["login"] = "Login cannot be null"
        if not old_password:
            errors["oldPassword"] = "Old Password cannot be null"
        if not new_password:
            errors["newPassword"] = "New Password cannot be null"
        if not confirm_password:
            errors["confirmPassword"] = "Confirm Password cannot be null"
        elif new_password and new_password != confirm_password:
            errors["confirmPassword"] = "New Password and Confirm Password do not match"
        if errors:
            return self.error_response(errors, "Validation failed", status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(login=login)
        except User.DoesNotExist:
            return self.error_response(None, "User not found", status.HTTP_404_NOT_FOUND)

        if user.password != old_password:
            return self.error_response({"oldPassword": "Old Password is incorrect"}, "Validation failed", status.HTTP_400_BAD_REQUEST)

        user.password = new_password
        UserService().save(user)

        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Password Changed Successfully"
        msg.text = EmailBuilder.change_password({"firstName": user.firstName, "login": user.login, "password": new_password})
        EmailService.send(msg)

        return self.error_response(None, "Password changed successfully", status.HTTP_200_OK)


class ForgotPasswordCtl(BaseRestCtl):
    """
    REST endpoint to trigger a forgot-password email.

    POST /ORSAPI/api/User/forgot-password/

    Request body:
        {
            "login": "user@example.com"
        }

    Responses:
        200 - Email sent   : {"error": false, "message": "Password reset email has been sent"}
        400 - Missing login: {"error": true,  "message": "Login cannot be null"}
        404 - Not found    : {"error": true,  "message": "No account found with this email"}
    """

    permission_classes = [AllowAny]

    def get_model(self):
        return User

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        login = request.data.get("login", "")

        if not login:
            return self.error_response(None, "Login cannot be null", status.HTTP_400_BAD_REQUEST)

        user_qs = ForgetPasswordService().search({"login": login})
        if user_qs.count() == 0:
            return self.error_response(None, "No account found with this email", status.HTTP_404_NOT_FOUND)

        user = user_qs[0]
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Forgot Password Request"
        msg.text = EmailBuilder.forgot_password({"firstName": user.firstName, "login": user.login, "password": user.password})
        EmailService.send(msg)

        return self.error_response(None, "Password reset email has been sent", status.HTTP_200_OK)


class UserRegistrationCtl(BaseRestCtl):
    """
    REST endpoint for new user self-registration.

    POST /ORSAPI/api/User/register/

    Request body:
        {
            "firstName": "John",
            "lastName":  "Doe",
            "login":     "john@example.com",
            "password":  "secret",
            "mobileNumber": "9876543210",
            "gender":    "Male",
            "dob":       "1990-01-25"   (optional, YYYY-MM-DD)
        }

    Responses:
        201 - Registered   : {"error": false, "message": "Registration successful", "data": {...user}}
        400 - Validation   : {"error": true,  "message": "Validation failed", "errors": {...}}
    """

    permission_classes = [AllowAny]

    def get_model(self):
        return User

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        data = request.data
        errors = {}

        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        login = data.get("login", "")
        password = data.get("password", "")
        mobile = data.get("mobileNumber", "")
        gender = data.get("gender", "Male")
        dob = data.get("dob", "")

        if not first_name:
            errors["firstName"] = "First Name cannot be null"
        if not last_name:
            errors["lastName"] = "Last Name cannot be null"
        if not login:
            errors["login"] = "Login cannot be null"
        elif "@" not in login or "." not in login:
            errors["login"] = "Login must be a valid email address"
        elif User.objects.filter(login=login).exists():
            errors["login"] = "This email is already registered"
        if not password:
            errors["password"] = "Password cannot be null"
        if not mobile:
            errors["mobileNumber"] = "Mobile Number cannot be null"
        elif not mobile.isdigit() or len(mobile) != 10:
            errors["mobileNumber"] = "Mobile Number must be 10 digits"
        if errors:
            return self.error_response(errors, "Validation failed", status.HTTP_400_BAD_REQUEST)

        user = User()
        user.firstName = first_name
        user.lastName = last_name
        user.login = login
        user.password = password
        user.mobileNumber = mobile
        user.gender = gender
        user.role_id = 2
        user.role_Name = ""
        user.dob = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
        UserService().save(user)

        msg = EmailMessage()
        msg.to = [login]
        msg.subject = "Welcome - Registration Successful"
        msg.text = EmailBuilder.sign_up({"firstName": first_name, "login": login, "password": password})
        EmailService.send(msg)

        return self.success_response(UserSerializers(user).data, "Registration successful", status.HTTP_201_CREATED)
    