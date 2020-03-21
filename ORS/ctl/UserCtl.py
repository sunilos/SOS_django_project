from django.http import HttpResponse
from .BaseCtl import BaseCtl

class UserCtl(BaseCtl):
    def __init__(self):
        self.name = ""
        self.address = ""

    def display(self,request,params={}):
        return HttpResponse("This is User display")  

    def submit(self,request,params={}):
        return HttpResponse("This is User submit")  
        



