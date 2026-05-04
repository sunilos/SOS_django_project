from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from ORS.utility.HtmlUtility import HtmlUtility


class UserListCtl(BaseCtl):

    def preload(self, request):
        role_list = RoleService().search({})
        gender_list = ["Male", "Female"]
        self.preload_data["role_select"] = HtmlUtility.get_list_from_beans(
            "role_id",
            int(self.form.get("role_id") or 0),
            role_list,
        )
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender", self.form.get("gender"), gender_list
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName", None)
        self.form["lastName"] = requestForm.get("lastName", None)
        self.form["login"] = requestForm.get("login", None)
        self.form["mobileNumber"] = requestForm.get("mobileNumber", None)
        self.form["gender"] = requestForm.get("gender", None)
        self.form["role_id"] = requestForm.get("role_id", None)

    def display(self, request, params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(
            request,
            self.get_template(),
            {"pageList": self.page_list, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(
            request,
            self.get_template(),
            {
                "pageList": self.page_list,
                "form": self.form,
                "preload_data": self.preload(request),
            },
        )
        return res

    def get_template(self):
        return "ors/UserList.html"

    def get_service(self):
        return UserService()
