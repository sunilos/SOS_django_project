from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import College
from service.service.CollegeService import CollegeService


class CollegeListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["name"] = requestForm.get("name", None)
        self.form["address"] = requestForm.get("address", None)
        self.form["state"] = requestForm.get("state", None)
        self.form["city"] = requestForm.get("city", None)
        self.form["phoneNumber"] = requestForm.get("phoneNumber", None)

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
        return "ors/CollegeList.html"

    # Service of College
    def get_service(self):
        return CollegeService()
