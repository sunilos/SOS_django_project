from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ORSAPI.restctl.CollegeListCtl import CollegeListCtl
from ORSAPI.restctl.CollegeCtl import CollegeCtl


# Create your views here.
def info(request,page,action ):
    print("REQ Method: ", request.method )
    print("Page: ", page)
    print("Action: ", action)
    print("Base Path: ", __file__)    

@csrf_exempt
def action(request,page, action = "" ):
    print("------------------>1")
    info(request,page,action)
    ctlName =  page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request,{"id":0})

'''
Calls respective controller with id
'''
@csrf_exempt
def actionId(request,page, id = 0 ):
    print("------------------>",id)    
    info(request,page,id)
    ctlName =  page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request,{"id":id})
