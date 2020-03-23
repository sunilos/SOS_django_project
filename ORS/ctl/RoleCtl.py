
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Role
from service.forms import RoleForm


class RoleCtl(BaseCtl):

    def populateRequest(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["name"] = requestForm["name"]
        self.form["description"] = requestForm["description"]

    def populateModel(self,obj):
        self.form["id"]  = obj.id 
        self.form["name"] = obj.name
        self.form["description"] = obj.description

    def inputValidation(self):
        super().inputValidation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["name"])):
            inputError["name"] = "Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["description"])):
            inputError["description"] = "Description can not be null"
            self.form["error"] = True
        return self.form["error"]        

    def display(self,request,params={}):
        rid = params["id"]
        if( rid > 0):
            r = Role.objects.get( id = rid )
            self.populateModel(r)
        res = render(request,self.getTemplate(), {"form":self.form})
        return res

    def submit(self,request,params={}):
        fm = RoleForm(request.POST)  
        fm.save()
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(request,self.getTemplate(),{"form":self.form})
        return res
        
    def getTemplate(self):
        return "ors/Role.html"          



