from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.FacultyService import FacultyService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from ORS.utility.HtmlUtility import HtmlUtility


class FacultyListCtl(BaseCtl):

    def preload(self, request):
        college_list = CollegeService().search({})
        course_list = CourseService().search({})
        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "college_ID",
            int(self.form.get("college_ID") or 0),
            college_list,
        )
        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "course_ID",
            int(self.form.get("course_ID") or 0),
            course_list,
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName", None)
        self.form["lastName"] = requestForm.get("lastName", None)
        self.form["email"] = requestForm.get("email", None)
        self.form["college_ID"] = requestForm.get("college_ID", None)
        self.form["course_ID"] = requestForm.get("course_ID", None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(
            request,
            self.get_template(),
            {"pageList": self.page_list, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(
            request,
            self.get_template(),
            {
                "pageList": self.page_list,
                "form": self.form,
                "preload_data": self.preload(request),
            },
        )
        return res

    def get_template(self):
        return "ors/FacultyList.html"

    def get_service(self):
        return FacultyService()
