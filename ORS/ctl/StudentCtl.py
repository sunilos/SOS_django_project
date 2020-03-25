
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Student
from service.forms import StudentForm
from service.service.StudentService import StudentService

class StudentCtl(BaseCtl):
    #Populate Form from HTTP Request 
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["dob"] = requestForm["dob"]
        self.form["mobileNumber"] = requestForm["mobileNumber"]
        self.form["email"] = requestForm["email"]
        self.form["college_ID"] = requestForm["college_ID"]
        self.form["collegeName"] = requestForm["collegeName"]

    #Populate Form from Model 
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"]  = obj.id
        self.form["firstName"] =obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["dob"] =obj.dob
        self.form["mobileNumber"] =obj.mobileNumber
        self.form["email"] =obj.email
        self.form["college_ID"] = obj.college_ID
        self.form["collegeName"] = obj.collegeName

    #Convert form into module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.firstName=self.form["firstName"]
        obj.lastName=self.form["lastName"] 
        obj.dob=self.form["dob"] 
        obj.mobileNumber=self.form["mobileNumber"] 
        obj.email=self.form["email"] 
        obj.college_ID=self.form["college_ID"] 
        obj.collegeName=self.form["collegeName"] 
        return obj

    #Validate form 
    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = " First_Name can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last_Name can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["mobileNumber"])):
            inputError["mobileNumber"] = "Mobile_Number can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["email"])):
            inputError["email"] = "email_id can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "college_ID can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["collegeName"])):
            inputError["collegeName"] = "college_Name can not be null"
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
        r = self.form_to_model(Student())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(request,self.get_template(),{"form":self.form})
        return res
        
    # Template html of Student page    
    def get_template(self):
        return "ors/Student.html"          

    # Service of Student     
    def get_service(self):
        return StudentService()        



