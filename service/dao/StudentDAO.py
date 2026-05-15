from service.models import Student
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class StudentDAO(BaseDAO):

    def apply_filters(self, q, params):
        val = params.get("firstName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(firstName__icontains=val)

        val = params.get("lastName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(lastName__icontains=val)

        val = params.get("dob", None)
        if DataValidator.isNotNull(val):
            q = q.filter(dob=val)

        val = params.get("mobileNumber", None)
        if DataValidator.isNotNull(val):
            q = q.filter(mobileNumber__icontains=val)

        val = params.get("email", None)
        if DataValidator.isNotNull(val):
            q = q.filter(email=val)

        val = params.get("college_ID", None)
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(college_ID=val)

        val = params.get("collegeName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(collegeName__icontains=val)

        return q

    def get_model(self):
        return Student
