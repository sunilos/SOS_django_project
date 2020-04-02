
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import College
from service.service.CollegeService import CollegeService
from rest_framework.parsers import JSONParser
from service.Serializers import CollegeSerializers

class CollegeCtl(BaseCtl):    
    def preload(self,request):
         self.preloadData=[{"name":"Madhya Pradesh","code":"MP"},{"name":"Uttar Pradesh","code":"UP"}]
        
    #Display College page 
    def display(self,request,params={}):
        if( params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(), {"form":self.form})
        return res

    #Submit College page
    def submit(self,request,params={}):
        parseData=JSONParser().parse(request)
        r=CollegeSerializers(data=parseData)
        self.get_service().save(r)
        res = render(request,self.get_template(),{"form":self.form})
        return res
        
    # Template html of Role page    
    def get_template(self):
        return "orsapi/College.html"          

    # Service of Role     
    def get_service(self):
        return CollegeService()        



