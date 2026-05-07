from service.dao.ForgetPasswordDAO import ForgetPasswordDAO
from .BaseService import BaseService


class ForgetPasswordService(BaseService):

    def get_dao(self):
        return ForgetPasswordDAO()
