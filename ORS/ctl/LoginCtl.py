from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect

class LoginCtl(BaseCtl):
    def __init__(self):
        self.name = ""
        self.address = ""

    def display(self,request,params={}):
        res = render(request,"Login.html")
        return res

    def submit(self,request,params={}):
        login = request.POST["loginId"]
        password = request.POST["password"]
        form = request.POST
        print('8888888888888888888>', form["loginId"], form["password"])
        message = ""
        print(login, password)

        if(login == "admin" and password == "admin"):
            res = redirect('/ORS/Welcome')
        else:
            message = "Invalid ID or Password"
            res = render(request,"Login.html",{"message":message, "form" :request.POST} )
        return res




