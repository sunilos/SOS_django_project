
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import CollegeForm
from service.models import College
from service.service.CollegeService import CollegeService
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from service.Serializers import CollegeSerializers


class CollegeListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        self.form["name"]=requestForm.get("name",None)
        self.form["address"]=requestForm.get("address",None)
        self.form["state"]=requestForm.get("state",None)
        self.form["city"]=requestForm.get("city",None)
        self.form["phoneNumber"]=requestForm.get("phoneNumber",None)

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




