from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#Import controller classes
from ORS.ctl.UserCtl import UserCtl
from ORS.ctl.AccountCtl import AccountCtl
from ORS.ctl.CollegeCtl import CollegeCtl
from ORS.ctl.LoginCtl import LoginCtl
from ORS.ctl.WelcomeCtl import WelcomeCtl
from ORS.ctl.RoleCtl import RoleCtl
from ORS.ctl.RoleListCtl import RoleListCtl
from ORS.ctl.FacultyCtl import FacultyCtl
from ORS.ctl.CourseCtl import CourseCtl
from ORS.ctl.StudentCtl import StudentCtl
from ORS.ctl.MarksheetCtl import MarksheetCtl
from ORS.ctl.SubjectCtl import SubjectCtl
from ORS.ctl.TimetableCtl import TimetableCtl

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


