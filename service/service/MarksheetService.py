from service.dao.MarksheetDAO import MarksheetDAO
from service.dao.StudentDAO import StudentDAO
from .BaseService import BaseService


class MarksheetService(BaseService):

    def save(self, obj):
        if obj.student_id and str(obj.student_id) != "0":
            student = StudentDAO().get(obj.student_id)
            if student is not None:
                obj.name = student.firstName + " " + student.lastName
        self._dao.save(obj)

    def get_dao(self):
        return MarksheetDAO()
