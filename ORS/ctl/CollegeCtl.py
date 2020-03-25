
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import College
from service.forms import CollegeForm
from service.service.CollegeService import CollegeService

class CollegeCtl(BaseCtl):    
    def preload(self,request):
         self.preloadData=[{"name":"Madhya Pradesh","code":"MP"},{"name":"Uttar Pradesh","code":"UP"}]
        

    #Populate Form from HTTP Request 
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["collegeName"] = requestForm["collegeName"]
        self.form["collegeAddress"] = requestForm["collegeAddress"]
        self.form["collegeState"] = requestForm["collegeState"]
        self.form["collegeCity"] = requestForm["collegeCity"]
        self.form["collegePhoneNumber"] = requestForm["collegePhoneNumber"]

    #Populate Form from Model 
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"]  = obj.id
        self.form["collegeName"] = obj.collegeName
        self.form["collegeAddress"] = obj.collegeAddress
        self.form["collegeState"] = obj.collegeState
        self.form["collegeCity"] = obj.collegeCity
        self.form["collegePhoneNumber"] = obj.collegePhoneNumber

    #Convert form into module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.collegeName=self.form["collegeName"]
        obj.collegeAddress=self.form["collegeAddress"] 
        obj.collegeState=self.form["collegeState"]
        obj.collegeCity=self.form["collegeCity"]
        obj.collegePhoneNumber=self.form["collegePhoneNumber"]
        return obj

    #Validate form 
    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["collegeName"])):
            inputError["collegeName"] = "Name can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["collegeAddress"])):
            inputError["collegeAddress"] = "Address can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["collegeState"])):
            inputError["collegeState"] = "State can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["collegeCity"])):
            inputError["collegeCity"] = "City can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["collegePhoneNumber"])):
            inputError["collegePhoneNumber"] = "PhoneNumber can not be null"
            self.form["error"] = True

        return self.form["error"]        

    #Display College page 
    def display(self,request,params={}):
        if( params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(), {"form":self.form})
        return res

    #Submit College page
    def submit(self,request,params={}):
        r = self.form_to_model(College())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(request,self.get_template(),{"form":self.form})
        return res
        
    # Template html of Role page    
    def get_template(self):
        return "ors/College.html"          

    # Service of Role     
    def get_service(self):
        return CollegeService()        



