from service.models import College
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Role business logics.   
'''
class CollegeService(BaseService):

    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("collegeName",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( collegeName = val)

        val = params.get("collegeAddress",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( collegeAddress = val)

        val = params.get("collegeState",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( collegeState = val)

        val = params.get("collegeCity",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( collegeCity = val)

        val = params.get("collegePhoneNumber",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( collegePhoneNumber = val)


        return q

    def get_model(self):
        return College
