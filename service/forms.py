from django import forms  
from .models import User, Role  

class UserForm(forms.ModelForm):  
    class Meta:  
        model = User  
        fields = "__all__"  

class RoleForm(forms.ModelForm):  
    class Meta:  
        model = Role  
        fields = "__all__"          