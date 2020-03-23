from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

def welcome(request):
    now = datetime.datetime.now()
    html = "<h1>Welcome in test app at %s.</h1>" % now
    return HttpResponse(html)

def info(request):
    now = datetime.datetime.now()
    html = "<h1>Info at %s.</h1>" % now
    html = html + "<p>Http Method: " + request.method 
    html = html + "<p>File Path: " + __file__ 
    res = HttpResponse(html)
    return res

def tempate(request):
    now = datetime.datetime.now()
    html = "<h1>Info at %s.</h1>" % now
    html = html + "<p>Http Method: " + request.method 
    html = html + "<p>File Path: " + __file__ 
    res = HttpResponse(html)
    return res
