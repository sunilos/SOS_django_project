from rest_framework import serializers
from service.models import College, Course, Role, User, Faculty, Marksheet, Student, Subject, TimeTable


class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FacultySerializers(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class MarksheetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Marksheet
        fields = "__all__"


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class TimeTableSerializers(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = "__all__"
