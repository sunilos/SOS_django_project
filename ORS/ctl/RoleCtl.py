
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Role
from service.forms import RoleForm
from service.service.RoleService import RoleService

class RoleCtl(BaseCtl):

    #Populate Form from HTTP Request 
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["name"] = requestForm["name"]
        self.form["description"] = requestForm["description"]

    #Populate Form from Model 
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"]  = obj.id 
        self.form["name"] = obj.name
        self.form["description"] = obj.description

    #Convert form into module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.name = self.form["name"]
        obj.description = self.form["description"]
        return obj

    #Validate form 
    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["name"])):
            inputError["name"] = "Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["description"])):
            inputError["description"] = "Description can not be null"
            self.form["error"] = True
        return self.form["error"]        

    #Display Role page 
    def display(self,request,params={}):
        if( params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(), {"form":self.form})
        return res

    #Submit Role page
    def submit(self,request,params={}):
        r = self.form_to_model(Role())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(request,self.get_template(),{"form":self.form})
        return res
        
    # Template html of Role page    
    def get_template(self):
        return "ors/Role.html"          

    # Service of Role     
    def get_service(self):
        return RoleService()        


