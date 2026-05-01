from service.models import Faculty
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService


class FacultyService(BaseService):

    def search(self, params):
        q = self.get_model().objects.filter()

        val = params.get("firstName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(firstName__icontains=val)

        val = params.get("lastName", None)
        if DataValidator.isNotNull(val):
            q = q.filter(lastName__icontains=val)

        val = params.get("email", None)
        if DataValidator.isNotNull(val):
            q = q.filter(email=val)

        val = params.get("college_ID", None)
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(college_ID=val)

        val = params.get("course_ID", None)
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(course_ID=val)

        return q

    def get_model(self):
        return Faculty
