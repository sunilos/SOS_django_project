from datetime import datetime
from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import TimeTable
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from ORS.utility.HtmlUtility import HtmlUtility


class TimeTableCtl(BaseCtl):

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
        self.form["id"] = request_form.get("id", 0)
        self.form["exam_date"] = request_form.get("examDate", "").strip()
        self.form["exam_time"] = request_form.get("examTime", "").strip()
        self.form["semester"] = request_form.get("semester", "").strip()
        self.form["course_id"] = request_form.get("courseId", 0)
        self.form["subject_id"] = request_form.get("subjectId", 0)

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["exam_date"] = obj.exam_date.strftime("%Y-%m-%d") if obj.exam_date else ""
        self.form["exam_time"] = obj.exam_time
        self.form["semester"] = obj.semester
        self.form["course_id"] = int(obj.course_id) if obj.course_id else 0
        self.form["subject_id"] = int(obj.subject_id) if obj.subject_id else 0

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.exam_date = (
            datetime.strptime(self.form.get("exam_date"), "%Y-%m-%d").date()
            if self.form.get("exam_date")
            else None
        )
        obj.exam_time = self.form.get("exam_time", "")
        obj.semester = self.form.get("semester", "")

        course_id = int(self.form.get("course_id") or 0)
        obj.course_id = course_id
        course = CourseService().get(course_id) if course_id > 0 else None
        obj.course_name = course.name if course else ""

        subject_id = int(self.form.get("subject_id") or 0)
        obj.subject_id = subject_id
        subject = SubjectService().get(subject_id) if subject_id > 0 else None
        obj.subject_name = subject.name if subject else ""

        return obj

    def input_validation(self):
        super().input_validation()
        input_error = self.form["inputError"]

        if DataValidator.isNull(self.form.get("exam_date")):
            input_error["exam_date"] = "Exam Date can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("exam_time")) or self.form.get("exam_time") == "0":
            input_error["exam_time"] = "Exam Time can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("semester")) or self.form.get("semester") == "0":
            input_error["semester"] = "Semester can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("course_id")) or str(self.form.get("course_id")) == "0":
            input_error["course_id"] = "Course can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("subject_id")) or str(self.form.get("subject_id")) == "0":
            input_error["subject_id"] = "Subject can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        timetable_id = int(params.get("id", 0))
        if timetable_id > 0:
            timetable = self.get_service().get(timetable_id)
            self.model_to_form(timetable)
        return render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request),
        })

    def submit(self, request, params={}):
        pk = int(self.form.get("id", 0) or 0)
        duplicate = self.get_service().get_model().objects.filter(
            exam_date=self.form.get("exam_date"),
            exam_time=self.form.get("exam_time"),
            semester=self.form.get("semester"),
            course_id=int(self.form.get("course_id") or 0),
            subject_id=int(self.form.get("subject_id") or 0),
        )
        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form["error"] = True
            self.form["message"] = "TimeTable already exist"
        else:
            timetable = self.form_to_model(TimeTable())
            self.get_service().save(timetable)
            self.form["id"] = timetable.id
            self.form["error"] = False
            self.form["message"] = "TimeTable updated successfully" if pk > 0 else "TimeTable added successfully..!!"

        return render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request),
        })

    def get_template(self):
        return "ors/TimeTable.html"

    def get_service(self):
        return TimeTableService()
