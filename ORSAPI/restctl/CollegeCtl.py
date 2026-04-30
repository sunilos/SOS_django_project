
from .BaseCtl import BaseCtl
from django.shortcuts import render
from django.http.response import JsonResponse
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
        serializer = CollegeSerializers(data=parseData)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "data": serializer.data,
                "error": False,
                "message": "Data is successfully saved",
            })
        return JsonResponse({
            "errors": serializer.errors,
            "error": True,
            "message": "Validation failed",
        }, status=400)
        
    # Template html of Role page    
    def get_template(self):
        return "orsapi/College.html"          

    # Service of Role     
    def get_service(self):
        return CollegeService()        



