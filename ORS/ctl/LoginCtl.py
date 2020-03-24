from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator

class LoginCtl(BaseCtl):

    def request_to_form(self,requestFrom):
        self.form["loginId"]  = requestFrom["loginId"]
        self.form["password"] = requestFrom["password"] 

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
        res = render(request,self.get_template())
        return res

    def submit(self,request,params={}):
        if(self.input_validation()):
            return render(request,self.get_template(),{"form":self.form})
        else:     
            if(self.form["loginId"]  == "admin" and self.form["password"] == "admin"):
                res = redirect('/ORS/Welcome')
            else:
                self.form["message"] = "Invalid ID or Password"
                res = render(request,self.get_template(),{"form":self.form})
        
        return res

    # Template html of Role page    
    def get_template(self):
        return "ors/Login.html"        

    # Service of Role     
    def get_service(self):
        return "RoleService()"        


