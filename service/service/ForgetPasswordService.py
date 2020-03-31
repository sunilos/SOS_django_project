from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Role business logics.   
'''
class ForgetPasswordService(BaseService):

    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("login",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( login = val)
        return q

    def get_model(self):
        return User
