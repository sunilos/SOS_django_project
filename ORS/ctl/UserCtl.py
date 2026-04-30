from django.db.models.manager import BaseManager
from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import Role, User
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from ORS.utility.HtmlUtility import HtmlUtility


class UserCtl(BaseCtl):
    """Controller for managing User CRUD operations."""

    def preload(self, request):
        """Load role list for the role dropdown before rendering the form."""
        role_list: BaseManager[Role] = RoleService().search(self.form)
        gender_list = ["Male", "Female"]
        self.preload_data["role_list"] = role_list
        self.preload_data["gender_list"] = gender_list

        self.preload_data["role_select"] = HtmlUtility.get_list_from_beans(
            "role_id",
            int(self.form.get("role_id") or 0),
            self.preload_data["role_list"],
        )
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender", self.form.get("gender"), self.preload_data["gender_list"]
        )
        print("a-------", self.form.get("gender"))
        return self.preload_data

    def request_to_form(self, requestForm):
        """Populate form dictionary from HTTP POST request data."""
        self.form["id"] = requestForm.get("id", 0)
        self.form["firstName"] = requestForm.get("firstName", "")
        self.form["lastName"] = requestForm.get("lastName", "")
        self.form["login"] = requestForm.get("login", "")
        self.form["password"] = requestForm.get("password", "")
        self.form["dob"] = requestForm.get("dob", "")
        self.form["mobileNumber"] = requestForm.get("mobileNumber", "")
        self.form["gender"] = requestForm.get("gender", "")
        self.form["role_id"] = requestForm.get("role_id", 0)

    def model_to_form(self, obj):
        """Populate form dictionary from a User model instance."""
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login"] = obj.login
        self.form["password"] = obj.password
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["mobileNumber"] = obj.mobileNumber
        self.form["gender"] = obj.gender
        self.form["role_id"] = int(obj.role_id) if obj.role_id else 0

    def form_to_model(self, obj):
        """Populate a User model instance from the form dictionary and return it."""
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form.get("firstName", "")
        obj.lastName = self.form.get("lastName", "")
        obj.login = self.form.get("login", "")
        obj.password = self.form.get("password", "")
        obj.dob = self.form.get("dob") or None
        obj.mobileNumber = self.form.get("mobileNumber", "")
        obj.gender = self.form.get("gender", "")
        obj.role_id = self.form.get("role_id", 0)
        return obj

    def input_validation(self):
        """Validate required fields and populate inputError messages. Returns True if any error exists."""
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
        else:
            if not DataValidator.isEmail(self.form.get("login")):
                inputError["login"] = "Login must be a valid email address"
                self.form["error"] = True

        if DataValidator.isNull(self.form.get("password")):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number can not be null"
            self.form["error"] = True
        else:
            if not DataValidator.isMobileNumber(self.form.get("mobileNumber")):
                inputError["mobileNumber"] = "Mobile Number must be 10 digits"
                self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        """Render the User form. Loads existing user data if a valid id is provided in params."""
        if params["id"] > 0:
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
            # self.preload(request);
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        """Save the User form data to the database and re-render the form with a success message."""
        r = self.form_to_model(User())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def get_template(self):
        """Return the template path for the User form."""
        return "ors/User.html"

    def get_service(self):
        """Return the UserService instance for database operations."""
        return UserService()
