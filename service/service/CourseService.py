from service.models import Course
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Course business logics.   
'''
class CourseService(BaseService):

    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("courseName",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( courseName = val)

        val = params.get("coursDescription",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( coursDescription = val)

        val = params.get("coursDuration",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( coursDuration = val)
        return q

    def get_model(self):
        return Course
