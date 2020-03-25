from service.models import Student
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Student business logics.   
'''
class StudentService(BaseService):
    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("firstName",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( firstName = val)

        val = params.get("lastName",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( lastName = val)

        val = params.get("dob",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( dob = val)

        val = params.get("mobileNumber",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( mobileNumber = val)

        val = params.get("email",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( email = val)

        val = params.get("college_ID",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( college_ID = val)

        val = params.get("collegeName",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( collegeName = val)
        return q

    def get_model(self):
        return Student
