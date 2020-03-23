from django.contrib import admin

# Register your models here.
from . models import User, Role

admin.site.register(Role)
admin.site.register(User)
