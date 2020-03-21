from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render


class WelcomeCtl(BaseCtl):

    def display(self,request,params={}):
        return render(request,"Welcome.html")

    def submit(self,request,params={}):
        return HttpResponse("This is Login submit")  
        



