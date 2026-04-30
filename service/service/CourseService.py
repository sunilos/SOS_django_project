from service.models import Course
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService


class CourseService(BaseService):

    def search(self, params):
        q = self.get_model().objects.filter()

        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            q = q.filter(name=val)

        val = params.get("description", None)
        if DataValidator.isNotNull(val):
            q = q.filter(description=val)

        val = params.get("duration", None)
        if DataValidator.isNotNull(val):
            q = q.filter(duration=val)

        return q

    def get_model(self):
        return Course
