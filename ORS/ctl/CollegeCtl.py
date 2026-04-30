
from django.http import HttpResponse
from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import College
from service.service.CollegeService import CollegeService


class CollegeCtl(BaseCtl):
    """Controller for managing College CRUD operations."""

    def preload(self, request):
        """Load college-related preload data for the college form."""
        state_list = ["Madhya Pradesh", "Uttar Pradesh"]
        self.preload_data["state_list"] = state_list
        return self.preload_data

    def request_to_form(self, requestForm):
        """Populate form dictionary from HTTP POST request data."""
        self.form["id"] = requestForm.get("id", 0)
        self.form["name"] = requestForm.get("name", "")
        self.form["address"] = requestForm.get("address", "")
        self.form["state"] = requestForm.get("state", "")
        self.form["city"] = requestForm.get("city", "")
        self.form["phoneNumber"] = requestForm.get("phoneNumber", "")

    def model_to_form(self, obj):
        """Populate form dictionary from a College model instance."""
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["address"] = obj.address
        self.form["state"] = obj.state
        self.form["city"] = obj.city
        self.form["phoneNumber"] = obj.phoneNumber

    def form_to_model(self, obj):
        """Populate a College model instance from the form dictionary."""
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.name = self.form.get("name", "")
        obj.address = self.form.get("address", "")
        obj.state = self.form.get("state", "")
        obj.city = self.form.get("city", "")
        obj.phoneNumber = self.form.get("phoneNumber", "")
        return obj

    def input_validation(self):
        """Validate required fields and populate inputError messages."""
        super().input_validation()
        inputError = self.form.get("inputError", {})

        if DataValidator.isNull(self.form.get("name")):
            inputError["name"] = "Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("address")):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("state")):
            inputError["state"] = "State can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("city")):
            inputError["city"] = "City can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("phoneNumber")):
            inputError["phoneNumber"] = "Phone Number can not be null"
            self.form["error"] = True
        else:
            if not DataValidator.isMobileNumber(self.form.get("phoneNumber")):
                inputError["phoneNumber"] = "Phone Number must be a mobile number (10 digits)"
                self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        """Render the College form, loading existing college data when an id is provided."""
        if params.get("id", 0) > 0:
            college = self.get_service().get(params["id"])
            self.model_to_form(college)
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        """Save the College form data and re-render the form with a success message."""
        college = self.form_to_model(College())
        self.get_service().save(college)
        self.form["id"] = college.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def get_template(self):
        """Return the template path for the College form."""
        return "ors/College.html"

    def get_service(self):
        """Return the CollegeService instance for database operations."""
        return CollegeService()



