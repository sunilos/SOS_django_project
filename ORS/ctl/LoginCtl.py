from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator

class LoginCtl(BaseCtl):

    def populateRequest(self,requestFrom):
        self.form["loginId"]  = requestFrom["loginId"]
        self.form["password"] = requestFrom["password"] 

    def inputValidation(self):
        super().inputValidation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["loginId"])):
            inputError["loginId"] = "Login can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self,request,params={}):
        res = render(request,self.getTemplate())
        return res

   
    def submit(self,request,params={}):
        if(self.inputValidation()):
            print("I am here ")
            return render(request,self.getTemplate(),{"form":self.form})
        else:     
            if(self.form["loginId"]  == "admin" and self.form["password"] == "admin"):
                res = redirect('/ORS/Welcome')
            else:
                self.form["message"] = "Invalid ID or Password"
                res = render(request,self.getTemplate(),{"form":self.form})
        
        return res

    def getTemplate(self):
        return "Login.html"        


