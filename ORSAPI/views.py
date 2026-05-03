from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def info(request,page,action ):
    print("REQ Method: ", request.method )
    print("Page: ", page)
    print("Action: ", action)
    print("Base Path: ", __file__)    

@csrf_exempt
def action(request,page, action = "get",id=0 ):
    print("---------->",id)
    info(request,page,action)
    methodCall =  page + "Ctl()."+action+"(request,{'id':id})"
    response = eval(methodCall)
    return response
