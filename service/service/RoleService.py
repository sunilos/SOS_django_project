from service.models import Role
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Role business logics.   
'''
class RoleService(BaseService):

    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("name",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( name = val)

        val = params.get("description",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( description = val)

        return q

    def get_model(self):
        return Role
