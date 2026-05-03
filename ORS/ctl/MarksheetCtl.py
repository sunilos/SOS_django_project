from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Marksheet
from service.service.MarksheetService import MarksheetService
from service.service.StudentService import StudentService
from ORS.utility.HtmlUtility import HtmlUtility


class MarksheetCtl(BaseCtl):
    """Controller for managing Marksheet CRUD operations."""

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
        """Populate form dictionary from HTTP POST request data."""
        self.form["id"] = requestForm.get("id", 0)
        self.form["rollNumber"] = requestForm.get("rollNumber", "")
        self.form["name"] = requestForm.get("name", "")
        self.form["physics"] = requestForm.get("physics", "")
        self.form["chemistry"] = requestForm.get("chemistry", "")
        self.form["maths"] = requestForm.get("maths", "")
        self.form["year"] = requestForm.get("year", "")
        self.form["student_id"] = requestForm.get("student_id", 0)

    def model_to_form(self, obj):
        """Populate form dictionary from a Marksheet model instance."""
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["rollNumber"] = obj.rollNumber
        self.form["name"] = obj.name
        self.form["physics"] = obj.physics
        self.form["chemistry"] = obj.chemistry
        self.form["maths"] = obj.maths
        self.form["year"] = obj.year
        self.form["student_id"] = int(obj.student_id) if obj.student_id else 0
        self.form["total"] = obj.total
        self.form["percentage"] = obj.percentage

    def form_to_model(self, obj):
        """Populate a Marksheet model instance from the form dictionary and return it."""
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.rollNumber = self.form.get("rollNumber", "")
        obj.name = self.form.get("name", "")
        obj.physics = int(self.form.get("physics") or 0)
        obj.chemistry = int(self.form.get("chemistry") or 0)
        obj.maths = int(self.form.get("maths") or 0)
        obj.year = int(self.form.get("year") or 0)
        obj.student_id = self.form.get("student_id", 0)
        return obj

    def input_validation(self):
        """Validate required fields and populate inputError messages. Returns True if any error exists."""
        super().input_validation()
        inputError = self.form.get("inputError", {})
        if DataValidator.isNull(self.form.get("rollNumber")):
            inputError["rollNumber"] = "Roll Number can not be null"
            self.form["error"] = True
        else:
            current_id = int(self.form.get("id") or 0)
            duplicate = Marksheet.objects.filter(rollNumber=self.form.get("rollNumber")).exclude(id=current_id).exists()
            if duplicate:
                inputError["rollNumber"] = "This Roll Number is already registered"
                self.form["error"] = True
        if DataValidator.isNull(self.form.get("physics")):
            inputError["physics"] = "Physics can not be null"
            self.form["error"] = True
        elif not DataValidator.isRange(self.form.get("physics"), 0, 100):
            inputError["physics"] = "Physics must be between 0 and 100"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("chemistry")):
            inputError["chemistry"] = "Chemistry can not be null"
            self.form["error"] = True
        elif not DataValidator.isRange(self.form.get("chemistry"), 0, 100):
            inputError["chemistry"] = "Chemistry must be between 0 and 100"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("maths")):
            inputError["maths"] = "Maths can not be null"
            self.form["error"] = True
        elif not DataValidator.isRange(self.form.get("maths"), 0, 100):
            inputError["maths"] = "Maths must be between 0 and 100"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("year")):
            inputError["year"] = "Year can not be null"
            self.form["error"] = True
        elif not DataValidator.isInteger(self.form.get("year")):
            inputError["year"] = "Year must be an integer"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("student_id")):
            inputError["student_id"] = "Student can not be null"
            self.form["error"] = True
        return self.form.get("error", False)

    def display(self, request, params={}):
        """Render the Marksheet form. Loads existing marksheet data if a valid id is provided in params."""
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
        """Save the Marksheet form data to the database and re-render the form with a success message."""
        r = self.form_to_model(Marksheet())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["total"] = r.total
        self.form["percentage"] = r.percentage
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def get_template(self):
        """Return the template path for the Marksheet form."""
        return "ors/Marksheet.html"

    def get_service(self):
        """Return the MarksheetService instance for database operations."""
        return MarksheetService()
