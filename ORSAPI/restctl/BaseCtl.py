from django.http import HttpResponse
from abc import ABC,abstractmethod
from django.shortcuts import render,redirect

'''
Base class is inherited by all application controllers 
'''
class BaseCtl(ABC):

    #Contains preload data
    preload_data = {}

    #Contains list of objects, it will be displayed at list page 
    page_list = {}

    '''
    Initialize controller attributes
    '''
    def __init__(self):
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
            self.request_to_form(request.POST)
            if(self.input_validation()):
                return render(request,self.get_template(),{"form":self.form})
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
    Populate values from Request POST/GET to Controller form object
    '''
    def request_to_form(self,requestFrom):
        pass

    #Populate Form from Model 
    def model_to_form(self,obj):
        pass

    #Convert form into module
    def form_to_model(self,obj):
        pass        

    '''
    Apply input validation 
    '''        
    def input_validation(self):
        self.form["error"] = False
        self.form["message"] = ""

    '''
    returns template of controller
    '''    
    @abstractmethod
    def get_template(self):
        pass

    @abstractmethod
    def get_service(self):
        pass
