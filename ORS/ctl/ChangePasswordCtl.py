from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.service.UserService import UserService
from .BaseCtl import BaseCtl
from service.service.EmailService import EmailService
from service.service.EmailBuilder import EmailBuilder
from service.service.EmailMessage import EmailMessage
from django.http import HttpResponse


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
            inputError["confirmPassword"] = "New Password and Confirm Password do not match"
            self.form["error"] = True
        return self.form["error"]

    def display(self, request, params={}):
        return render(request, self.get_template(), {"form": self.form})

    def submit(self, request, params={}):
        login_id = request.session.get("loginId")
        user = self.get_service().get(login_id)
        if user is None:
            self.form["error"] = True
            self.form["message"] = "Session expired. Please login again."
            return render(request, self.get_template(), {"form": self.form})
        if user.password != self.form.get("oldPassword"):
            self.form["inputError"]["oldPassword"] = "Old Password is incorrect"
            self.form["error"] = True
            return render(request, self.get_template(), {"form": self.form})
        user.password = self.form.get("newPassword")
        self.get_service().save(user)
        self.form["error"] = False
        self.form["message"] = "Password changed successfully"
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Password Changed Successfully"
        msg.text = EmailBuilder.change_password({"firstName": user.firstName, "login": user.login, "password": self.form.get("newPassword")})
        EmailService.send(msg)
        
        return render(request, self.get_template(), {"form": self.form})

    def get_template(self):
        return "ors/ChangePassword.html"

    def get_service(self):
        return UserService()
    
