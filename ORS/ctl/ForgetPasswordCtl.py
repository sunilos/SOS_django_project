from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from service.service.ForgetPasswordService import ForgetPasswordService
from service.service.EmailService import EmailService
from service.service.EmailBuilder import EmailBuilder
from service.service.EmailMessage import EmailMessage

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
            user_qs = self.get_service().search(self.form)
            print("============",user_qs)
            if(user_qs.count() == 0):
                self.form["message"] = "Invalid ID"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                user = user_qs[0]
                request.session["user"] = user.login
                msg = EmailMessage()
                msg.to = [user.login]
                msg.subject = "Forgot Password Request"
                msg.text = EmailBuilder.forgot_password({"login": user.login})
                EmailService.send(msg)
                self.form["message"] = "Password reset email has been sent"
                res = render(request,self.get_template(),{"form":self.form})
        return res

    # Template html of Role page    
    def get_template(self):
        return "ors/ForgetPassword.html"        

    # Service of Role     
    def get_service(self):
        return ForgetPasswordService()        


