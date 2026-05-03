from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.models import User
from service.Serializers import UserSerializers
from service.service.UserService import UserService
from service.service.ForgetPasswordService import ForgetPasswordService
from service.service.EmailService import EmailService
from service.service.EmailBuilder import EmailBuilder
from service.service.EmailMessage import EmailMessage


class UserCtl(APIView):
    """REST controller for User CRUD operations."""

    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response(
                    {"error": True, "message": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = UserSerializers(user)
        else:
            serializer = UserSerializers(User.objects.all(), many=True)
        return Response({"error": False, "data": serializer.data})

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "User saved successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": True, "message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "message": "User updated successfully", "data": serializer.data}
            )
        return Response(
            {"error": True, "message": "Validation failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": True, "message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        user.delete()
        return Response({"error": False, "message": "User deleted successfully"})


class UserLoginCtl(APIView):
    """
    REST endpoint for user authentication.

    POST /ORSAPI/api/User/login/

    Request body:
        {
            "login": "user@example.com",
            "password": "yourpassword"
        }

    Responses:
        200 - Valid credentials   : {"error": false, "message": "Login successful", "data": {...user}}
        400 - Missing fields      : {"error": true,  "message": "Login and password are required"}
        401 - Wrong credentials   : {"error": true,  "message": "Invalid login or password"}
    """

    def post(self, request):
        login = request.data.get("login", "")
        password = request.data.get("password", "")

        if not login or not password:
            return Response(
                {"error": True, "message": "Login and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = UserService().authenticate({"login": login, "password": password})
        if user is None:
            return Response(
                {"error": True, "message": "Invalid login or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = UserSerializers(user)
        return Response({"error": False, "message": "Login successful", "data": serializer.data})


class ChangePasswordCtl(APIView):
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
            return Response(
                {"error": True, "message": "Validation failed", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(login=login)
        except User.DoesNotExist:
            return Response(
                {"error": True, "message": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.password != old_password:
            return Response(
                {"error": True, "message": "Validation failed", "errors": {"oldPassword": "Old Password is incorrect"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.password = new_password
        UserService().save(user)

        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Password Changed Successfully"
        msg.text = EmailBuilder.change_password({"firstName": user.firstName, "login": user.login, "password": new_password})
        EmailService.send(msg)

        return Response({"error": False, "message": "Password changed successfully"})


class ForgotPasswordCtl(APIView):
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

    def post(self, request):
        login = request.data.get("login", "")

        if not login:
            return Response(
                {"error": True, "message": "Login cannot be null"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_qs = ForgetPasswordService().search({"login": login})
        if user_qs.count() == 0:
            return Response(
                {"error": True, "message": "No account found with this email"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = user_qs[0]
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Forgot Password Request"
        msg.text = EmailBuilder.forgot_password({"firstName": user.firstName, "login": user.login, "password": user.password})
        EmailService.send(msg)

        return Response({"error": False, "message": "Password reset email has been sent"})


class UserRegistrationCtl(APIView):
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
            return Response(
                {"error": True, "message": "Validation failed", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from datetime import datetime
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

        serializer = UserSerializers(user)
        return Response(
            {"error": False, "message": "Registration successful", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
