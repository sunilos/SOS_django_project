
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import CourseForm
from service.models import  Course
from service.service.CourseService import CourseService

class CourseListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        self.form["courseName"] = requestForm.get( "courseName", None)
        self.form["courseDescription"] =  requestForm.get( "courseDescription", None) 
        self.form["courseDuration"] =  requestForm.get( "courseDuration", None) 


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
        return "ors/CourseList.html"          

    # Service of Role     
    def get_service(self):
        return CourseService()        




