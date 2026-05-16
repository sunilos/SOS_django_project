from service.models import Subject
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class SubjectDAO(BaseDAO):

    def apply_filters(self, q, params):
        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            q = q.filter(subjectName__icontains=val)

        val = params.get("description", None)
        if DataValidator.isNotNull(val):
            q = q.filter(subjectDescription__icontains=val)

        val = params.get("course_id", None)
        if DataValidator.isNotNull(val) and str(val) != "0":
            q = q.filter(course_ID=val)

        return q

    def get_model(self):
        return Subject
