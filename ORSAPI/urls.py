"""SOSWebProjects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .rest.CollegeCtl import CollegeCtl
from .rest.StudentCtl import StudentCtl
from .rest.CourseCtl import CourseCtl
from .rest.FacultyCtl import FacultyCtl
from .rest.RoleCtl import RoleCtl
from .rest.MarksheetCtl import MarksheetCtl
from .rest.UserCtl import UserCtl, UserLoginCtl, ChangePasswordCtl, ForgotPasswordCtl, UserRegistrationCtl

urlpatterns = [
    # REST API routes — must be before the generic catch-all patterns
    path('api/College/', CollegeCtl.as_view()),
    path('api/College/<int:id>/', CollegeCtl.as_view()),
    path('api/Student/', StudentCtl.as_view()),
    path('api/Student/<int:id>/', StudentCtl.as_view()),
    path('api/Course/', CourseCtl.as_view()),
    path('api/Course/<int:id>/', CourseCtl.as_view()),
    path('api/Faculty/', FacultyCtl.as_view()),
    path('api/Faculty/<int:id>/', FacultyCtl.as_view()),
    path('api/Role/', RoleCtl.as_view()),
    path('api/Role/<int:id>/', RoleCtl.as_view()),
    path('api/Marksheet/', MarksheetCtl.as_view()),
    path('api/Marksheet/<int:id>/', MarksheetCtl.as_view()),
    path('api/User/', UserCtl.as_view()),
    path('api/User/<int:id>/', UserCtl.as_view()),
    path('api/User/login/', UserLoginCtl.as_view()),
    path('api/User/change-password/', ChangePasswordCtl.as_view()),
    path('api/User/forgot-password/', ForgotPasswordCtl.as_view()),
    path('api/User/register/', UserRegistrationCtl.as_view()),
]
