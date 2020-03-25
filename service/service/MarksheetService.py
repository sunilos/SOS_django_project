from service.models import Marksheet
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Role business logics.   
'''
class MarksheetService(BaseService):

    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("rollNumber",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( rollNumber = val)

        val = params.get("name",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( name = val)

        val = params.get("physics",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( physics = val)

        val = params.get("chemistry",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( chemistry = val)

        val = params.get("maths",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( maths = val)

        val = params.get("student_ID",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( student_ID = val)

        return q

    def get_model(self):
        return Marksheet
