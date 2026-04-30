from service.models import College
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Role business logics.   
'''
class CollegeService(BaseService):

    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("name",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( name = val)

        val = params.get("address",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( address = val)

        val = params.get("state",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( state = val)

        val = params.get("city",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( city = val)

        val = params.get("phoneNumber",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( phoneNumber = val)


        return q

    def get_model(self):
        return College
