from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains User business logics.   
'''
class ChangePasswordService(BaseService):

    def authenticate(self,params):
        userList = self.search(params)
        if (userList.count() > 0):
            print("8888888->", userList[0].login)
            return userList[0]
        else:
            return None
     
    def get_model(self):
        return User
