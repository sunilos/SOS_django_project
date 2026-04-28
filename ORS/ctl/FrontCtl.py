
from django.http import HttpResponse
from django.shortcuts import render,redirect

class FrontCtl:    

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        print("-------------------> ", request.path.find("auth/"))
        print("-------------------> ", ( request.path.find("auth/") > -1))
        if( request.path.find("auth/") == -1):
            user = request.session.get("user",None)
            if(user is None):
                res = redirect('/ORS/auth/Login')
                return res

        # Code to be executed for each request before
        # the view (and later middleware) are called.
                
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response        



