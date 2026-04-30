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

    def save(self, obj):
        if(obj.id == 0):
            obj.id = None
        obj.save()
        
       
    def delete(self,id):
        r = self.get(id)
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



