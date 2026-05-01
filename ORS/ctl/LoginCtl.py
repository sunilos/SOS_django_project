from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from service.service.UserService import UserService

class LoginCtl(BaseCtl):

    def request_to_form(self,requestFrom):
        self.form["loginId"]  = requestFrom["loginId"]
        self.form["password"]   = requestFrom["password"]
        self.form["rememberMe"] = requestFrom.get("rememberMe", False)

    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["loginId"])):
            inputError["loginId"] = "Login can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self,request,params={}):
        request.session.flush()
        return render(request,self.get_template())

    def submit(self,request,params={}):
        if(self.input_validation()):
            return render(request,self.get_template(),{"form":self.form})
        else:     
            user = self.get_service().authenticate(self.form)
            if(user is None):
                self.form["message"] = "Invalid ID or Password"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                if self.form.get("rememberMe"):
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                    request.session.set_expiry(0)  # expires when browser closes
                request.session["user"] = user.login
                request.session["loginId"] = user.id
                request.session["firstName"] = user.firstName
                request.session["lastName"] = user.lastName
                res = redirect('/ORS/Welcome')
        return res

    # Template html of Role page    
    def get_template(self):
        return "ors/Login.html"        

    # Service of Role     
    def get_service(self):
        return UserService()        


