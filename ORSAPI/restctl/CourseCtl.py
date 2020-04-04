
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Course
from service.forms import CourseForm
from service.service.CourseService import CourseService
from rest_framework.parsers import JSONParser
from service.Serializers import CourseSerializers
from django.http.response import JsonResponse
import json
from django.core import serializers

class CourseCtl(): 
    def get(self,request, params = {}):
        service=CourseService()
        c=service.get(params["id"])
        res={}
        if(c!=None):
            res["data"]=c.to_json()
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"data":res})

    def delete(self,request, params = {}):
        service=CourseService()
        c=service.get(params["id"])
        res={}
        if(c!=None):
            service.delete(params["id"])
            res["data"]=c.to_json()
            res["error"]=False
            res["message"]="Data is Successfully deleted"
        else:
            res["error"]=True
            res["message"]="Data is not deleted"
        return JsonResponse({res})

    def search(self,request, params = {}):
        service=CourseService()
        c=service.search()
        res={}
        data=[]
        for x in c:
            data.append(x.to_json())
        if(c!=None):
            res["data"]=data
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"data":res})

    def form_to_model(self,obj,request):
        pk = int(request["id"])
        if(pk>0):
            obj.id = pk
        obj.courseName = request["courseName"]
        obj.courseDescription = request["courseDescription"]
        obj.courseDuration=request["courseDuration"] 
        return obj

    def save(self,request, params = {}):        
        json_request=json.loads(request.body)     
        r=self.form_to_model(Course(), json_request)
        service=CourseService()
        c=service.save(r)
        res={}
        if(r!=None):
            res["data"]=r.to_json()
            res["error"]=False
            res["message"]="Data is Successfully saved"
        else:
            res["error"]=True
            res["message"]="Data is not saved"
        return JsonResponse({"data":res})

    # Template html of Role page    
    def get_template(self):
        return "orsapi/Course.html"          

    # Service of Role     
    def get_service(self):
        return CourseService()        


       



