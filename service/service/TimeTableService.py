from service.dao.TimeTableDAO import TimeTableDAO
from .BaseService import BaseService


class TimeTableService(BaseService):

    def get_dao(self):
        return TimeTableDAO()
