from abc import ABC,abstractmethod

class BaseService(ABC):
    def __init__(self):
        print("0")

    def get(self, rid):
        try:
            r = self.get_model().objects.get( id = rid )
            return r
        except self.get_model().DoesNotExist :
            return None

    def search(self):
        try:
            r = self.get_model().objects.all()
            return r
        except self.get_model().DoesNotExist :
            return None

    def save(self,role):
        if(role.id == 0):
            role.id = None
        role.save()
        
       
    def delete(self,rid):
        r = self.get(rid)
        r.delete()       

    def find_by_unique_key(self, rid):
        try:
            r = self.get_model().objects.get( id = rid )
            return r
        except self.get_model().DoesNotExist :
            return None



    @abstractmethod
    def get_model(self):
        pass



