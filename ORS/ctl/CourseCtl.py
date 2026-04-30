from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import Course
from service.service.CourseService import CourseService


class CourseCtl(BaseCtl):
    """Controller for managing Course CRUD operations."""

    def preload(self, _request):
        """Load preload data required by the Course page before rendering."""
        return self.preload_data

    def request_to_form(self, requestForm):
        """Populate form dictionary from HTTP POST request data."""
        self.form["id"] = requestForm.get("id", 0)
        self.form["name"] = requestForm.get("name", "")
        self.form["description"] = requestForm.get("description", "")
        self.form["duration"] = requestForm.get("duration", "")

    def model_to_form(self, obj):
        """Populate form dictionary from a Course model instance."""
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description
        self.form["duration"] = obj.duration

    def form_to_model(self, obj):
        """Populate a Course model instance from the form dictionary."""
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.name = self.form.get("name", "")
        obj.description = self.form.get("description", "")
        obj.duration = self.form.get("duration", "")
        return obj

    def input_validation(self):
        """Validate required fields and populate inputError messages."""
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form.get("name")):
            inputError["name"] = "Name can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("description")):
            inputError["description"] = "Description can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("duration")):
            inputError["duration"] = "Duration can not be null"
            self.form["error"] = True
        return self.form["error"]

    def display(self, request, params={}):
        """Render the Course form, loading existing course data when an id is provided."""
        if params["id"] > 0:
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form, "preload_data": self.preload(request)})
        return res

    def submit(self, request, _params={}):
        """Save the Course form data and re-render the form with a success message."""
        r = self.form_to_model(Course())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(request, self.get_template(), {"form": self.form, "preload_data": self.preload(request)})
        return res

    def get_template(self):
        """Return the template path for the Course form."""
        return "ors/Course.html"

    def get_service(self):
        """Return the CourseService instance for database operations."""
        return CourseService()
