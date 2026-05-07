from django.shortcuts import render
from service.service.UserService import UserService
from service.utility.DataValidator import DataValidator
from service.service.ForgetPasswordService import ForgetPasswordService
from .BaseCtl import BaseCtl


class ForgetPasswordCtl(BaseCtl):

    def request_to_form(self, requestFrom):
        self.form["loginId"] = requestFrom.get("loginId", "")

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form.get("loginId")):
            inputError["loginId"] = "Login can not be null"
            self.form["error"] = True
        return self.form["error"]

    def display(self, request, params={}):
        return render(request, self.get_template(), {"form": self.form})

    def submit(self, request, params={}):
        if self.input_validation():
            return render(request, self.get_template(), {"form": self.form})
        else:
            loginId = self.form.get("loginId")
            userObj = self.get_service().forgot_password(loginId)
            if userObj is None:
                self.form["message"] = "Login ID does not exist"
            else:
                self.form["message"] = "Password reset email has been sent"
        res = render(request, self.get_template(), {"form": self.form})
        return res

    # Template html of Role page
    def get_template(self):
        return "ors/ForgetPassword.html"

    # Service of Role
    def get_service(self):
        return UserService()
