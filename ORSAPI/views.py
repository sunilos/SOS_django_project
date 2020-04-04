from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ORSAPI.restctl.CollegeListCtl import CollegeListCtl
from ORSAPI.restctl.CollegeCtl import CollegeCtl
from ORSAPI.restctl.CourseCtl import CourseCtl
from ORSAPI.restctl.CourseListCtl import CourseListCtl

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
