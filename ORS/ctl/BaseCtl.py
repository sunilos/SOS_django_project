from django.http import HttpResponse
from abc import ABC,abstractmethod

'''
Base class is inherited by all application controllers 
'''
class BaseCtl(ABC):
    preloadData={}

    def __init__(self):
        self.id = 0

    '''
    It loads preload data of the page 
    '''
    def preload(self,request):
        print("This is preload")

    '''
    execute method is executed for each HTTP request.  
    It in turn calls display() or submit() method for 
    HTTP GET and HTTP POST methods 
    '''
    def execute(self,request, params = {}):
        print("This is execute")
        self.preload(request)
        if("GET" ==  request.method):
            return self.display(request, params) 
        elif ("POST" ==  request.method):
            return self.submit(request,params) 
        else:
            message = "Request is not supported"
            return HttpResponse(message)          

    '''
    Displays rceord of received ID    
    '''
    @abstractmethod
    def display(self,request,params = {}):
        pass 

    '''
    Submit data 
    '''
    @abstractmethod
    def submit(self,request,params = {}):
        pass            

