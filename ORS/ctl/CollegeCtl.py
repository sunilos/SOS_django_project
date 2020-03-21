
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render

class CollegeCtl(BaseCtl):
    def __init__(self):
        self.name = ""
        self.address = ""
    
    def preload(self,request):
         self.preloadData=[{"name":"Madhya Pradesh","code":"MP"},{"name":"Uttar Pradesh","code":"UP"}]
        

    def display(self,request,params={}):
        print(self.preloadData)
        return render(request,"College.html",{"stateList":self.preloadData})  

    def submit(self,request,params={}):
        return HttpResponse("This is College submit")  
