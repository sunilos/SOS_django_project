
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import CollegeForm
from service.models import College
from service.service.CollegeService import CollegeService
from service.Serializers import CollegeSerializers
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


class CollegeListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        self.form["collegeName"]=requestForm.get("collegeName",None)
        self.form["collegeAddress"]=requestForm.get("collegeAddress",None)
        self.form["collegeState"]=requestForm.get("collegeState",None)
        self.form["collegeCity"]=requestForm.get("collegeCity",None)
        self.form["collegePhoneNumber"]=requestForm.get("collegePhoneNumber",None)

    def display(self,request,params={}):
        list= self.get_service().search(self.form)
        self.page_list=CollegeSerializers(list,many=True)
        res = JsonResponse({"pageList":self.page_list.data},safe=False)
        return res

    def submit(self,request,params={}):
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list, "form":self.form})
        return res
        
    def get_template(self):
        return "ors/CollegeList.html"          

    # Service of College     
    def get_service(self):
        return CollegeService()        




