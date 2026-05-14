import os
import uuid
from datetime import datetime

from django.conf import settings
from django.shortcuts import redirect, render

from ORS.utility.HtmlUtility import HtmlUtility
from service.models import Role, User
from service.service.RoleService import RoleService
from service.service.UserService import UserService
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from django.db.models.manager import BaseManager


class ProfileCtl(BaseCtl):
    """Controller for viewing and updating the logged-in user's profile."""

    def preload(self, request):
        role_list: BaseManager[Role] = RoleService().search(self.form)
        self.preload_data["role_list"] = role_list
        self.preload_data["role_select"] = HtmlUtility.get_list_from_beans(
            "role_id",
            int(self.form.get("role_id") or 0),
            self.preload_data["role_list"],
        )
        gender_list = ["Male", "Female"]
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender", self.form.get("gender"), gender_list
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["firstName"] = requestForm.get("firstName", "")
        self.form["lastName"] = requestForm.get("lastName", "")
        self.form["login"] = requestForm.get("login", "")
        self.form["dob"] = requestForm.get("dob", "")
        self.form["mobileNumber"] = requestForm.get("mobileNumber", "")
        self.form["gender"] = requestForm.get("gender", "")
        self.form["role_Name"] = requestForm.get("role_Name", "")
        self.form["photo"] = requestForm.get("photo", "")

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login"] = obj.login
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["mobileNumber"] = obj.mobileNumber
        self.form["gender"] = obj.gender
        self.form["role_id"] = obj.role_id
        self.form["role_Name"] = obj.role_Name
        self.form["photo"] = obj.photo or ""

    def form_to_model(self, obj):
        obj.firstName = self.form.get("firstName", "")
        obj.lastName = self.form.get("lastName", "")
        obj.login = self.form.get("login", "")
        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        obj.mobileNumber = self.form.get("mobileNumber", "")
        obj.gender = self.form.get("gender", "")
        obj.photo = self.form.get("photo", "")
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form.get("inputError", {})

        if DataValidator.isNull(self.form.get("firstName")):
            inputError["firstName"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("lastName")):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("login")):
            inputError["login"] = "Login can not be null"
            self.form["error"] = True
        elif not DataValidator.isEmail(self.form.get("login")):
            inputError["login"] = "Login must be a valid email address"
            self.form["error"] = True
        else:
            current_id = int(self.form.get("id") or 0)
            duplicate = (
                User.objects.filter(login=self.form.get("login"))
                .exclude(id=current_id)
                .exists()
            )
            if duplicate:
                inputError["login"] = "This email is already registered"
                self.form["error"] = True

        if DataValidator.isNull(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number can not be null"
            self.form["error"] = True
        elif not DataValidator.isMobileNumber(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        user = self._get_current_user(request)
        if user is None:
            return redirect("/ORS/auth/Login")
        self.model_to_form(user)
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    def submit(self, request, params={}):
        user = self._get_current_user(request)
        if user is None:
            return redirect("/ORS/auth/Login")

        self.form["id"] = user.id
        self.form["password"] = user.password
        self.form["role_id"] = user.role_id
        self.form["role_Name"] = user.role_Name
        self.form["photo"] = user.photo or ""

        photo_file = request.FILES.get("photo")
        if photo_file:
            ext = os.path.splitext(photo_file.name)[1].lower()
            filename = f"profile_{uuid.uuid4().hex}{ext}"
            dest_dir = os.path.join(settings.MEDIA_ROOT, settings.USER_PHOTO_DIR)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)
            with open(dest_path, "wb+") as f:
                for chunk in photo_file.chunks():
                    f.write(chunk)
            self.form["photo"] = f"{settings.USER_PHOTO_DIR}/{filename}"

        updated_user = self.form_to_model(user)
        self.get_service().save(updated_user)

        request.session["user"] = updated_user.login
        request.session["loginId"] = updated_user.id
        request.session["firstName"] = updated_user.firstName
        request.session["lastName"] = updated_user.lastName

        self.model_to_form(updated_user)
        self.update_from(False, "Profile updated successfully")
        return render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )

    def _get_current_user(self, request):
        login_id = request.session.get("loginId")
        if not login_id:
            return None
        return self.get_service().get(login_id)

    def get_template(self):
        return "ors/Profile.html"

    def get_service(self):
        return UserService()
