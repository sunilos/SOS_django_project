from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Subject
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService
from ORS.utility.HtmlUtility import HtmlUtility


class SubjectCtl(BaseCtl):

    def preload(self, request):
        course_list = CourseService().search({})
        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "course_id",
            int(self.form.get("course_id") or 0),
            course_list,
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["name"] = requestForm.get("name", "")
        self.form["description"] = requestForm.get("description", "")
        self.form["course_id"] = requestForm.get("course_id", 0)

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.subjectName
        self.form["description"] = obj.subjectDescription
        self.form["course_id"] = int(obj.course_ID) if obj.course_ID else 0

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.subjectName = self.form.get("name", "")
        obj.subjectDescription = self.form.get("description", "")

        course_id = int(self.form.get("course_id") or 0)
        obj.course_ID = course_id
        course = CourseService().get(course_id) if course_id > 0 else None
        obj.courseName = course.name if course else ""

        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]

        if DataValidator.isNull(self.form.get("name")):
            inputError["name"] = "Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("description")):
            inputError["description"] = "Description can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("course_id")) or str(self.form.get("course_id")) == "0":
            inputError["course_id"] = "Course can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        if params.get("id", 0) > 0:
            obj = self.get_service().get(params["id"])
            self.model_to_form(obj)
        return render(request, self.get_template(), {"form": self.form, "preload_data": self.preload(request)})

    def submit(self, request, params={}):
        pk = int(self.form.get("id", 0) or 0)
        duplicate = self.get_service().get_model().objects.filter(
            subjectName=self.form.get("name", ""),
            course_ID=int(self.form.get("course_id") or 0),
        )
        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form["error"] = True
            self.form["message"] = "Subject already exists for this course"
        else:
            obj = self.form_to_model(Subject())
            self.get_service().save(obj)
            self.form["id"] = obj.id
            self.form["error"] = False
            self.form["message"] = "Subject updated successfully" if pk > 0 else "Subject added successfully"
        return render(request, self.get_template(), {"form": self.form, "preload_data": self.preload(request)})

    def get_template(self):
        return "ors/Subject.html"

    def get_service(self):
        return SubjectService()
