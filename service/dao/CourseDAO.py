from service.models import Course
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class CourseDAO(BaseDAO):

    def search(self, params):
        q = self.get_model().objects.filter()

        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            q = q.filter(name__icontains=val)

        val = params.get("description", None)
        if DataValidator.isNotNull(val):
            q = q.filter(description__icontains=val)

        val = params.get("duration", None)
        if DataValidator.isNotNull(val):
            q = q.filter(duration__icontains=val)

        return q

    def get_model(self):
        return Course
