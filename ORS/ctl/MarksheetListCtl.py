from django.shortcuts import render

from ORS.utility.HtmlUtility import HtmlUtility
from service.service.StudentService import StudentService
from .BaseCtl import BaseCtl
from service.service.MarksheetService import MarksheetService


class MarksheetListCtl(BaseCtl):

    def preload(self, request):
        """Load student list for the student dropdown before rendering the form."""
        student_list = StudentService().search(self.form)
        self.preload_data["student_list"] = student_list
        self.preload_data["student_select"] = HtmlUtility.get_list_from_beans(
            "student_id",
            int(self.form.get("student_id") or 0),
            self.preload_data["student_list"],
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["rollNumber"] = requestForm.get("rollNumber", None)
        self.form["name"] = requestForm.get("name", None)
        self.form["student_id"] = requestForm.get("student_id", None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        return render(
            request,
            self.get_template(),
            {"pageList": self.page_list, "preload_data": self.preload(request)},
        )

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        return render(
            request,
            self.get_template(),
            {
                "pageList": self.page_list,
                "form": self.form,
                "preload_data": self.preload(request),
            },
        )

    def get_template(self):
        return "ors/MarksheetList.html"

    def get_service(self):
        return MarksheetService()
