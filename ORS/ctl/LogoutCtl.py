from .BaseCtl import BaseCtl
from django.shortcuts import redirect


class LogoutCtl(BaseCtl):

    def display(self, request, _params={}):
        request.session.flush()
        return redirect('/ORS/Login')

    def submit(self, request, _params={}):
        request.session.flush()
        return redirect('/ORS/Login')

    def get_template(self):
        return "ors/Login.html"

    def get_service(self):
        pass
