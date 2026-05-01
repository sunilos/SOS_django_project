from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.FacultyService import FacultyService


class FacultyListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName", None)
        self.form["lastName"] = requestForm.get("lastName", None)
        self.form["email"] = requestForm.get("email", None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {"pageList": self.page_list})
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def get_template(self):
        return "ors/FacultyList.html"

    def get_service(self):
        return FacultyService()
