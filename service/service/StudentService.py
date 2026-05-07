from service.dao.StudentDAO import StudentDAO
from .BaseService import BaseService


class StudentService(BaseService):

    def get_dao(self):
        return StudentDAO()
