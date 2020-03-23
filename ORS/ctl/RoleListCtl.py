
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import RoleForm, UserForm
from service.models import User, Role

class RoleListCtl(BaseCtl):

    def populateRequest(self,requestForm):
        self.form["name"] = requestForm["name"]
        self.form["description"] = requestForm["description"]

    def display(self,request,params={}):
        self.pageList = Role.objects.all()
        res = render(request,self.getTemplate(),{"pageList":self.pageList})
        return res

    def submit(self,request,params={}):
        print("--------------------->",self.form["name"]) 
        self.pageList = Role.objects.all().filter(name = self.form["name"] )
        res = render(request,self.getTemplate(),{"pageList":self.pageList})
        return res
        
    def getTemplate(self):
        return "ors/RoleList.html"          



