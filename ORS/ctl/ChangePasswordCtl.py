
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import User
from service.service.ChangePasswordService import ChangePasswordService

class ChangePasswordCtl(BaseCtl):    
    #Populate Form from HTTP Request 
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["newPassword"] = requestForm["newPassword"]
        self.form["oldPassword"] = requestForm["newPassword"]
        self.form["confirmPassword"] = requestForm["confirmPassword"]
 
    #Populate Form from Model 
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"]  = obj.id
        self.form["newPassword"] = obj.newPassword
        self.form["oldPassword"] = obj.oldPassword
        self.form["confirmPassword"] = obj.confirmPassword

    #Convert form into module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.newPassword=self.form["newPassword"]
        obj.oldPassword=self.form["oldPassword"] 
        obj.confirmPassword=self.form["confirmPassword"]
        return obj

    #Validate form 
    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["newPassword"])):
            inputError["newPassword"] = "newPassword can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["oldPassword"])):
            inputError["oldPassword"] = "oldPassword can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["confirmPassword"])):
            inputError["confirmPassword"] = "confirmPassword can not be null"
            self.form["error"] = True
        return self.form["error"]        

    #Display Change Password page 
    def display(self,request,params={}):
        if( params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(), {"form":self.form})
        return res

    #Submit Change Password page
    def submit(self,request,params={}):
        user = request.session.get("user",None)
        if(user is not None):
            self.form["message"] = "Welcome " + user.login
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(request,self.get_template(),{"form":self.form})
        return res
        
    # Template html of Change Password page    
    def get_template(self):
        return "ors/ChangePassword.html"          

    # Service of Role     
    def get_service(self):
        return ChangePasswordService()        



