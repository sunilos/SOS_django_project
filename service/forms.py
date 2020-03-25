from django import forms  
from .models import User, Role,College

class UserForm(forms.ModelForm):  
    class Meta:  
        model = User  
        fields = "__all__"  

class RoleForm(forms.ModelForm):  
    class Meta:  
        model = Role  
        fields = "__all__"         
        
class CollegeForm(forms.ModelForm):  
    class Meta:  
        model = College  
        fields = "__all__"          
