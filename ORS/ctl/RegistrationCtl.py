from datetime import datetime
from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import User
from service.service.UserService import UserService
from ORS.utility.HtmlUtility import HtmlUtility
from service.service.EmailService import EmailService
from service.service.EmailBuilder import EmailBuilder
from service.service.EmailMessage import EmailMessage


class RegistrationCtl(BaseCtl):

    def preload(self, request):
        gender_list = ["Male", "Female"]
        self.preload_data["gender_list"] = gender_list
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender", self.form.get("gender"), gender_list
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["firstName"] = requestForm.get("firstName", "")
        self.form["lastName"] = requestForm.get("lastName", "")
        self.form["login"] = requestForm.get("login", "")
        self.form["password"] = requestForm.get("password", "")
        self.form["dob"] = requestForm.get("dob", "")
        self.form["mobileNumber"] = requestForm.get("mobileNumber", "")
        self.form["gender"] = requestForm.get("gender", "")
        self.form["role_id"] = 2

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login"] = obj.login
        self.form["password"] = obj.password
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["mobileNumber"] = obj.mobileNumber
        self.form["gender"] = obj.gender
        self.form["role_id"] = obj.role_id

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form.get("firstName", "")
        obj.lastName = self.form.get("lastName", "")
        obj.login = self.form.get("login", "")
        obj.password = self.form.get("password", "")
        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        obj.mobileNumber = self.form.get("mobileNumber", "")
        obj.gender = self.form.get("gender", "")
        obj.role_id = self.form.get("role_id", 2)
        obj.role_Name = ""
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

        if DataValidator.isNull(self.form.get("password")):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number can not be null"
            self.form["error"] = True
        elif not DataValidator.isMobileNumber(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        if params.get("id", 0) > 0:
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form, "preload_data": self.preload(request)})
        return res

    def submit(self, request, params={}):
        r = self.form_to_model(User())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Registration successful"
        msg = EmailMessage()
        msg.to = [self.form["login"]]
        msg.subject = "Welcome - Registration Successful"
        msg.text = EmailBuilder.sign_up({"firstName": self.form["firstName"], "login": self.form["login"], "password": self.form["password"]})
        EmailService.send(msg)
        res = render(request, self.get_template(), {"form": self.form, "preload_data": self.preload(request)})
        return res

    def get_template(self):
        return "ors/Registration.html"

    def get_service(self):
        return UserService()
