
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Marksheet
from service.forms import MarksheetForm
from service.service.MarksheetService import MarksheetService

class MarksheetCtl(BaseCtl):
    #Populate Form from HTTP Request 
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["rollNumber"] = requestForm["rollNumber"]
        self.form["name"] = requestForm["name"]
        self.form["physics"] = requestForm["physics"]
        self.form["chemistry"] = requestForm["chemistry"]
        self.form["maths"] = requestForm["maths"]
        self.form["student_ID"] = requestForm["student_ID"]

    #Populate Form from Model 
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"]  = obj.id 
        self.form["rollNumber"] = obj.rollNumber
        self.form["name"] = obj.name
        self.form["physics"] = obj.physics
        self.form["chemistry"] = obj.chemistry
        self.form["maths"] = obj.maths
        self.form["student_ID"] = obj.student_ID

    #Convert form into module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.rollNumber=self.form["rollNumber"]
        obj.name=self.form["name"]
        obj.physics=self.form["physics"] 
        obj.chemistry=self.form["chemistry"] 
        obj.maths=self.form["maths"] 
        obj.student_ID=self.form["student_ID"]
        return obj

    #Validate form 
    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["rollNumber"])):
            inputError["rollNumber"] = "roll Number can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["name"])):
            inputError["name"] = "name can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["physics"])):
            inputError["physics"] = "physics can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["chemistry"])):
            inputError["chemistry"] = "chemistry can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["maths"])):
            inputError["maths"] = "maths can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["student_ID"])):
            inputError["student_ID"] = "student_ID can not be null"
            self.form["error"] = True

        return self.form["error"]        

    #Display Marksheet page 
    def display(self,request,params={}):
        if( params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(), {"form":self.form})
        return res

    #Submit Marksheet page
    def submit(self,request,params={}):
        r = self.form_to_model(Marksheet())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(request,self.get_template(),{"form":self.form})
        return res
        
    # Template html of Role page    
    def get_template(self):
        return "ors/Marksheet.html"          

    # Service of Role     
    def get_service(self):
        return MarksheetService()        



