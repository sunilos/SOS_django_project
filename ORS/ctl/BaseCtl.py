from django.http import HttpResponse
from abc import ABC,abstractmethod
from django.shortcuts import render,redirect

'''
Base class is inherited by all application controllers 
'''
class BaseCtl(ABC):
    preloadData = {}

    '''
    Initialize controller attributes
    '''
    def __init__(self):
        self.id = 0
        self.form = {}
        self.form["id"] = 0
        self.form["message"] = ""
        self.form["error"] = False
        self.form["inputError"] = {}


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
            self.populateRequest(request.POST)
            if(self.inputValidation()):
                return render(request,self.getTemplate(),{"form":self.form})
            else:
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
    '''
    returns template of controller
    '''    

    @abstractmethod
    def getTemplate(self):
        pass

    '''
    Populate values from Request POST/GET to Controller form object
    '''
    def populateRequest(self,requestFrom):
        pass

    '''
    Apply input validation 
    '''        
    def inputValidation(self):
        self.form["error"] = False
        self.form["message"] = ""


