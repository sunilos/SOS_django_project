from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains User business logics.   
'''
class UserService(BaseService):

    def authenticate(self,params):
        userList = self.search(params)
        if (userList.count() > 0):
            print("8888888->", userList[0].login)
            return userList[0]
        else:
            return None
     
    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("firstName",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( firstName = val)

        val = params.get("lastName",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( lastName = val)

        val = params.get("login",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( login = val)

        val = params.get("password",None)
        if( DataValidator.isNotNull(val)):
            q= q.filter( password = val)

        return q

    def get_model(self):
        return User
