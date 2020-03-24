from django.contrib import admin

# Register your models here.
from . models import User, Role, College,Course,Marksheet,student, subject, timeTable

admin.site.register(Role)
admin.site.register(User)
admin.site.register(College)
admin.site.register(Course)
admin.site.register(Marksheet)
admin.site.register(student)
admin.site.register(subject)
admin.site.register(timeTable)
