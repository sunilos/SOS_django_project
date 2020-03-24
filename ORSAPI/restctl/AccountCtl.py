from django.http import HttpResponse
from .BaseCtl import BaseCtl

class AccountCtl(BaseCtl):
    def __init__(self):
        super(AccountCtl, self).__init__()

    def display(self,request,params={}):
        if(params["id"] > 0 ):
            print("Param ----->", params["id"])
        return HttpResponse("This is ACC display {0}" )  

    def submit(self,request,params={}):
        return HttpResponse("This is AC submit {0}" , params["id"])  
        



