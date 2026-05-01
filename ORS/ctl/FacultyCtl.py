from datetime import datetime
from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Faculty
from service.service.FacultyService import FacultyService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from ORS.utility.HtmlUtility import HtmlUtility


class FacultyCtl(BaseCtl):

    def preload(self, request):
        college_list = CollegeService().search({})
        course_list = CourseService().search({})
        gender_list = ["Male", "Female"]

        self.preload_data["college_list"] = college_list
        self.preload_data["course_list"] = course_list
        self.preload_data["gender_list"] = gender_list

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
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender", self.form.get("gender"), gender_list
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["firstName"] = requestForm.get("firstName", "")
        self.form["lastName"] = requestForm.get("lastName", "")
        self.form["email"] = requestForm.get("email", "")
        self.form["mobileNumber"] = requestForm.get("mobileNumber", "")
        self.form["address"] = requestForm.get("address", "")
        self.form["gender"] = requestForm.get("gender", "")
        self.form["dob"] = requestForm.get("dob", "")
        self.form["college_ID"] = requestForm.get("college_ID", 0)
        self.form["course_ID"] = requestForm.get("course_ID", 0)
        self.form["subjectName"] = requestForm.get("subjectName", "")

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["email"] = obj.email
        self.form["mobileNumber"] = obj.mobileNumber
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["college_ID"] = int(obj.college_ID) if obj.college_ID else 0
        self.form["course_ID"] = int(obj.course_ID) if obj.course_ID else 0
        self.form["subjectName"] = obj.subjectName

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form.get("firstName", "")
        obj.lastName = self.form.get("lastName", "")
        obj.email = self.form.get("email", "")
        obj.mobileNumber = self.form.get("mobileNumber", "")
        obj.address = self.form.get("address", "")
        obj.gender = self.form.get("gender", "")
        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        college_id = int(self.form.get("college_ID") or 0)
        obj.college_ID = college_id
        college = CollegeService().get(college_id) if college_id > 0 else None
        obj.collegeName = college.name if college else ""

        course_id = int(self.form.get("course_ID") or 0)
        obj.course_ID = course_id
        course = CourseService().get(course_id) if course_id > 0 else None
        obj.courseName = course.name if course else ""

        obj.subjectName = self.form.get("subjectName", "")
        obj.subject_ID = 0
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form.get("inputError", {})

        if DataValidator.isNull(self.form.get("firstName")):
            inputError["firstName"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("lastName")):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("email")):
            inputError["email"] = "Email can not be null"
            self.form["error"] = True
        elif not DataValidator.isEmail(self.form.get("email")):
            inputError["email"] = "Email must be a valid email address"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number can not be null"
            self.form["error"] = True
        elif not DataValidator.isMobileNumber(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("address")):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        if params.get("id", 0) > 0:
            faculty = self.get_service().get(params["id"])
            self.model_to_form(faculty)
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        faculty = self.form_to_model(Faculty())
        self.get_service().save(faculty)
        self.form["id"] = faculty.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def get_template(self):
        return "ors/Faculty.html"

    def get_service(self):
        return FacultyService()
