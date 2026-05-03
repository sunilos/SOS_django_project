from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Student
from service.Serializers import StudentSerializers


class StudentCtl(BaseRestCtl):
    def get_model(self):
        return Student

    def get_serializer_class(self):
        return StudentSerializers
