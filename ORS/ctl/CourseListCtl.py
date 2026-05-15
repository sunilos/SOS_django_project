from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.CourseService import CourseService


class CourseListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["name"] = requestForm.get("name", None)
        self.form["description"] = requestForm.get("description", None)
        self.form["duration"] = requestForm.get("duration", None)
        self.form["page_number"] = int(requestForm.get("page_number", 1))

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form, page_number=1)
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        page_number = self.form.get("page_number", 1)
        self.page_list = self.get_service().search(self.form, page_number=page_number)
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def get_template(self):
        return "ors/CourseList.html"

    def get_service(self):
        return CourseService()
