from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from service.service.ForgetPasswordService import ForgetPasswordService

class ForgetPasswordCtl(BaseCtl):

    def request_to_form(self,requestFrom):
        self.form["loginId"]  = requestFrom["loginId"]
    
    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["loginId"])):
            inputError["loginId"] = "Login can not be null"
            self.form["error"] = True
        return self.form["error"]

    def display(self,request,params={}):
        res = render(request,self.get_template())
        return res

    def submit(self,request,params={}):
        if(self.input_validation()):
            return render(request,self.get_template(),{"form":self.form})
        else:     
            user = self.get_service().search(self.form)
            print("============",user[0].login)
            if(user is None):
                self.form["message"] = "Invalid ID"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                request.session["user"] = user
                res = redirect('/ORS/Login')
        return res

    # Template html of Role page    
    def get_template(self):
        return "ors/ForgetPassword.html"        

    # Service of Role     
    def get_service(self):
        return ForgetPasswordService()        


