from datetime import datetime

from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import Student
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService
from ORS.utility.HtmlUtility import HtmlUtility


class StudentCtl(BaseCtl):
    """Controller for managing Student CRUD operations."""

    def preload(self, request):
        """Load college list for the college dropdown before rendering the form."""
        college_list = CollegeService().search({})

        self.preload_data["college_list"] = college_list

        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "college_ID",
            int(self.form.get("college_ID") or 0),
            self.preload_data["college_list"],
        )

        return self.preload_data

    def request_to_form(self, requestForm):
        """Populate form dictionary from HTTP POST request data."""
        self.form["id"] = requestForm.get("id", 0)
        self.form["firstName"] = requestForm.get("firstName", "")
        self.form["lastName"] = requestForm.get("lastName", "")
        self.form["dob"] = requestForm.get("dob", "")
        self.form["mobileNumber"] = requestForm.get("mobileNumber", "")
        self.form["email"] = requestForm.get("email", "")
        self.form["college_ID"] = requestForm.get("college_ID", 0)
        self.form["collegeName"] = requestForm.get("collegeName", "")

    def model_to_form(self, obj):
        """Populate form dictionary from a Student model instance."""
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["mobileNumber"] = obj.mobileNumber
        self.form["email"] = obj.email
        self.form["college_ID"] = int(obj.college_ID) if obj.college_ID else 0
        self.form["collegeName"] = obj.collegeName

    def form_to_model(self, obj):
        """Populate a Student model instance from the form dictionary."""
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form.get("firstName", "")
        obj.lastName = self.form.get("lastName", "")
        #obj.dob = self.form.get("dob") or None
        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        obj.mobileNumber = self.form.get("mobileNumber", "")
        obj.email = self.form.get("email", "")
        obj.college_ID = self.form.get("college_ID", 0)
        obj.collegeName = self.get_college_name(obj.college_ID)
        return obj

    def input_validation(self):
        """Validate required fields and populate inputError messages."""
        super().input_validation()
        inputError = self.form.get("inputError", {})
        if DataValidator.isNull(self.form.get("firstName")):
            inputError["firstName"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("lastName")):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("dob")):
            inputError["dob"] = "Date Of Birth can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number can not be null"
            self.form["error"] = True
        elif not DataValidator.isMobileNumber(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("email")):
            inputError["email"] = "Email can not be null"
            self.form["error"] = True
        elif not DataValidator.isEmail(self.form.get("email")):
            inputError["email"] = "Email must be a valid email address"
            self.form["error"] = True

        if (
            DataValidator.isNull(self.form.get("college_ID"))
            or self.form.get("college_ID") == "0"
        ):
            inputError["college_ID"] = "College can not be null"
            self.form["error"] = True
        elif self.get_college_name(self.form.get("college_ID")) == "":
            inputError["college_ID"] = "Please select a valid college"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        """Render the Student form, loading existing student data when an id is provided."""
        if params["id"] > 0:
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        """Save the Student form data and re-render the form with a success message."""
        r = self.form_to_model(Student())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        self.model_to_form(r)
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def get_college_name(self, college_id):
        """Return the college name for the selected college id."""
        if DataValidator.isNull(college_id):
            return ""
        college = CollegeService().get(college_id)
        if college is None:
            return ""
        return college.name

    def get_template(self):
        """Return the template path for the Student form."""
        return "ors/Student.html"

    def get_service(self):
        """Return the StudentService instance for database operations."""
        return StudentService()
