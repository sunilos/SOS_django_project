from service.models import Marksheet
from service.service.StudentService import StudentService
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService


class MarksheetService(BaseService):

    def save(self, obj):
        if obj.id == 0:
            obj.id = None
        if obj.student_id and str(obj.student_id) != "0":
            stdObj = StudentService().get(obj.student_id)
            if stdObj is not None:
                obj.name = stdObj.firstName + " " + stdObj.lastName
        obj.save()

    def search(self, params):
        q = self.get_model().objects.filter()

        val = params.get("rollNumber", None)
        if DataValidator.isNotNull(val):
            q = q.filter(rollNumber=val)

        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            q = q.filter(name=val)

        val = params.get("physics", None)
        if DataValidator.isNotNull(val):
            q = q.filter(physics=val)

        val = params.get("chemistry", None)
        if DataValidator.isNotNull(val):
            q = q.filter(chemistry=val)

        val = params.get("maths", None)
        if DataValidator.isNotNull(val):
            q = q.filter(maths=val)

        val = params.get("student_id", None)
        if DataValidator.isNotNull(val):
            q = q.filter(student_id=val)

        return q

    def get_model(self):
        return Marksheet
