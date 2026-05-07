from service.dao.CollegeDAO import CollegeDAO
from .BaseService import BaseService


class CollegeService(BaseService):

    def get_dao(self):
        return CollegeDAO()
