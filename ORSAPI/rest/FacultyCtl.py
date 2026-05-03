from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Faculty
from service.Serializers import FacultySerializers


class FacultyCtl(BaseRestCtl):
    def get_model(self):
        return Faculty

    def get_serializer_class(self):
        return FacultySerializers
