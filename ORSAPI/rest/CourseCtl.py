from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Course
from service.Serializers import CourseSerializers


class CourseCtl(BaseRestCtl):
    def get_model(self):
        return Course

    def get_serializer_class(self):
        return CourseSerializers
