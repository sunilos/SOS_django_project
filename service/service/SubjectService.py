from service.dao.SubjectDAO import SubjectDAO
from .BaseService import BaseService


class SubjectService(BaseService):

    def get_dao(self):
        return SubjectDAO()
