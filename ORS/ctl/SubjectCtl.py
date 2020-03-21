
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render

class SubjectCtl(BaseCtl):
    def __init__(self):
        self.name = ""
        self.address = ""        

    def display(self,request,params={}):
        print(self.preloadData)
        return HttpResponse("This is Subject Display")  

    def submit(self,request,params={}):
        return HttpResponse("This is Subject submit")  
        



