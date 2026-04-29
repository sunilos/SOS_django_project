
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from service.service.RoleService import RoleService

class RoleListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        self.form["name"] = requestForm.get( "name", None)
        self.form["description"] =  requestForm.get( "description", None) 

    def display(self,request,params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list})
        return res

    def submit(self,request,params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list, "form":self.form})
        return res
        
    def get_template(self):
        return "ors/RoleList.html"          

    # Service of Role     
    def get_service(self):
        return RoleService()        




