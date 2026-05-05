from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.service.UserService import UserService
from .BaseCtl import BaseCtl


class ChangePasswordCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["oldPassword"] = requestForm.get("oldPassword", "")
        self.form["newPassword"] = requestForm.get("newPassword", "")
        self.form["confirmPassword"] = requestForm.get("confirmPassword", "")

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form.get("oldPassword")):
            inputError["oldPassword"] = "Old Password cannot be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("newPassword")):
            inputError["newPassword"] = "New Password cannot be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("confirmPassword")):
            inputError["confirmPassword"] = "Confirm Password cannot be null"
            self.form["error"] = True
        elif self.form.get("newPassword") != self.form.get("confirmPassword"):
            inputError["confirmPassword"] = (
                "New Password and Confirm Password do not match"
            )
            self.form["error"] = True
        return self.form["error"]

    def display(self, request, params={}):
        return render(request, self.get_template(), {"form": self.form})

    def submit(self, request, params={}):
        login_id = request.session.get("loginId")
        service = self.get_service()
        user = service.get(login_id)
        if user is None:
            self.update_from(True, "Session expired. Please login again.")
            return render(request, self.get_template(), {"form": self.form})
        if user.password != self.form.get("oldPassword"):
            self.update_from(True, "Old Password is incorrect.")
            return render(request, self.get_template(), {"form": self.form})

        service.change_password(user.login, self.form.get("newPassword"))

        self.update_from(False, "Password changed successfully")
        return render(request, self.get_template(), {"form": self.form})

    def get_template(self):
        return "ors/ChangePassword.html"

    def get_service(self):
        return UserService()
