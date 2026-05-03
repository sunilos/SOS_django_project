from django.db import models
from abc import ABCMeta, abstractmethod


class ModelABCMeta(type(models.Model), ABCMeta):
    """Combined metaclass resolving the conflict between Django's ModelBase and ABCMeta."""

    pass


class DropdownItem(metaclass=ModelABCMeta):
    """Mixin that enforces a standard key/value interface for dropdown lists."""

    @abstractmethod
    def get_key(self):
        pass

    @abstractmethod
    def get_value(self):
        pass


# Create your models here.
class Role(models.Model, DropdownItem):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = "SOS_ROLE"


class User(models.Model, DropdownItem):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    login = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)
    role_id = models.IntegerField()
    role_Name = models.CharField(max_length=50)
    mobileNumber = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, default="Male")
    photo = models.CharField(max_length=200, blank=True, default="")

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.firstName} {self.lastName}"

    class Meta:
        db_table = "SOS_USER"


class College(models.Model, DropdownItem):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = "SOS_COLLEGE"


class BaseModel(models.Model):
    def to_json(self):
        data = {}
        return data


class Course(models.Model, DropdownItem):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    def to_json(self):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
        }
        return data

    class Meta:
        db_table = "SOS_COURSE"


class Faculty(models.Model, DropdownItem):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    mobileNumber = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.firstName} {self.lastName}"

    class Meta:
        db_table = "SOS_FACULTY"


class Marksheet(models.Model, DropdownItem):
    rollNumber = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    maths = models.IntegerField()
    year = models.IntegerField()
    student_id = models.IntegerField()

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.name} - {self.rollNumber}"

    @property
    def total(self):
        return self.physics + self.chemistry + self.maths

    @property
    def percentage(self):
        return round((self.total / 300) * 100, 2)

    class Meta:
        db_table = "SOS_MARKSHEET"


class Student(models.Model, DropdownItem):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    mobileNumber = models.CharField(max_length=20)
    email = models.EmailField()
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.firstName} {self.lastName}"

    class Meta:
        db_table = "SOS_STUDENT"


class Subject(models.Model, DropdownItem):
    subjectName = models.CharField(max_length=50)
    subjectDescription = models.CharField(max_length=50)
    dob = models.DateField()
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.subjectName

    class Meta:
        db_table = "SOS_SUBJECT"


class TimeTable(models.Model, DropdownItem):
    examTime = models.DateTimeField()
    examDate = models.DateField()
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return (
            f"{self.courseName} - {self.subjectName} - {self.examDate} {self.examTime}"
        )

    class Meta:
        db_table = "SOS_TIMETABLE"
