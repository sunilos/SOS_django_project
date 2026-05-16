from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService
from ORS.utility.HtmlUtility import HtmlUtility


class SubjectListCtl(BaseCtl):

    def preload(self, request):
        course_list = CourseService().search({})
        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "course_id",
            int(self.form.get("course_id") or 0),
            course_list,
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["name"] = requestForm.get("name", None)
        self.form["description"] = requestForm.get("description", None)
        self.form["course_id"] = requestForm.get("course_id", None)
        self.form["page_number"] = int(requestForm.get("page_number", 1) or 1)

    def display(self, request, params={}):
        page_list = self.get_service().search(self.form, page_number=1)
        return render(
            request,
            self.get_template(),
            {"page_list": page_list, "form": self.form, "preload_data": self.preload(request)},
        )

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        page_number = int(self.form.get("page_number", 1))
        page_list = self.get_service().search(self.form, page_number=page_number)
        return render(
            request,
            self.get_template(),
            {"page_list": page_list, "form": self.form, "preload_data": self.preload(request)},
        )

    def get_template(self):
        return "ors/SubjectList.html"

    def get_service(self):
        return SubjectService()
