from service.dao.FacultyDAO import FacultyDAO
from .BaseService import BaseService


class FacultyService(BaseService):

    def get_dao(self):
        return FacultyDAO()
