
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import StudentForm
from service.models import Student
from service.service.StudentService import StudentService

class StudentListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        self.form["firstName"]=requestForm.get("firstName",None)
        self.form["lastName"]=requestForm.get("lastName",None)
        self.form["dob"]=requestForm.get("dob",None)
        self.form["mobileNumber"]=requestForm.get("mobileNumber",None)
        self.form["email"]=requestForm.get("email",None)
        self.form["college_ID"]=requestForm.get("college_ID",None)
        self.form["collegeName"]=requestForm.get("collegeName",None)

    def display(self,request,params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list})
        return res

    def submit(self,request,params={}):
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list, "form":self.form})
        return res
        
    def get_template(self):
        return "ors/StudentList.html"          

    # Service of Marksheet     
    def get_service(self):
        return StudentService()        




