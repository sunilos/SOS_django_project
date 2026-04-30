from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.MarksheetService import MarksheetService


class MarksheetListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["rollNumber"] = requestForm.get("rollNumber", None)
        self.form["name"] = requestForm.get("name", None)
        self.form["student_id"] = requestForm.get("student_id", None)

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
        return "ors/MarksheetList.html"

    def get_service(self):
        return MarksheetService()
