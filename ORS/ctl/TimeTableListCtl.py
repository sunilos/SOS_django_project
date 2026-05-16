from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from ORS.utility.HtmlUtility import HtmlUtility


class TimeTableListCtl(BaseCtl):

    def preload(self, request):
        exam_time_list = [
            "08:00 AM to 11:00 AM",
            "12:00 PM to 03:00 PM",
            "04:00 PM to 07:00 PM",
        ]
        semester_list = ["1", "2", "3", "4", "5", "6", "7", "8"]
        course_list = CourseService().search({})
        subject_list = SubjectService().search({})

        self.preload_data["exam_time_select"] = HtmlUtility.get_list_from_list(
            "examTime", self.form.get("exam_time"), exam_time_list
        )
        self.preload_data["semester_select"] = HtmlUtility.get_list_from_list(
            "semester", self.form.get("semester"), semester_list
        )
        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "courseId", int(self.form.get("course_id") or 0), course_list
        )
        self.preload_data["subject_select"] = HtmlUtility.get_list_from_beans(
            "subjectId", int(self.form.get("subject_id") or 0), subject_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["exam_date"] = request_form.get("examDate", "")
        self.form["exam_time"] = request_form.get("examTime", "")
        self.form["semester"] = request_form.get("semester", "")
        self.form["course_id"] = request_form.get("courseId", 0)
        self.form["subject_id"] = request_form.get("subjectId", 0)
        self.form["page_number"] = int(request_form.get("page_number", 1) or 1)

    def display(self, request, params={}):
        page_list = self.get_service().search(self.form, page_number=1)
        return render(request, self.get_template(), {
            "form": self.form,
            "page_list": page_list,
            "preload_data": self.preload(request),
        })

    def submit(self, request, params={}):
        page_number = int(self.form.get("page_number", 1))
        page_list = self.get_service().search(self.form, page_number=page_number)
        return render(request, self.get_template(), {
            "form": self.form,
            "page_list": page_list,
            "preload_data": self.preload(request),
        })

    def get_template(self):
        return "ors/TimeTableList.html"

    def get_service(self):
        return TimeTableService()
