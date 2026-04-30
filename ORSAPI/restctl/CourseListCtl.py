
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.forms import CourseForm
from service.models import  Course
from service.service.CourseService import CourseService

class CourseListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        self.form["name"] = requestForm.get( "name", None)
        self.form["description"] =  requestForm.get( "description", None) 
        self.form["duration"] =  requestForm.get( "duration", None) 


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
        return "orsapi/CourseList.html"          

    # Service of Role     
    def get_service(self):
        return CourseService()        




