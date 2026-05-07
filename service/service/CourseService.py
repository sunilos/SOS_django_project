from service.dao.CourseDAO import CourseDAO
from .BaseService import BaseService


class CourseService(BaseService):

    def get_dao(self):
        return CourseDAO()
