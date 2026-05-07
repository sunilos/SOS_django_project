from service.dao.RoleDAO import RoleDAO
from .BaseService import BaseService


class RoleService(BaseService):

    def get_dao(self):
        return RoleDAO()
