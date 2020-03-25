from django import forms  
from .models import User, Role,College,Course,Faculty,Marksheet,Student,Subject,TimeTable

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

class CourseForm(forms.ModelForm):  
    class Meta:  
        model = Course  
        fields = "__all__"          

class FacultyForm(forms.ModelForm):  
    class Meta:  
        model = Faculty  
        fields = "__all__"          

class MarksheetForm(forms.ModelForm):  
    class Meta:  
        model = Marksheet  
        fields = "__all__"          
      
class StudentForm(forms.ModelForm):  
    class Meta:  
        model = Student  
        fields = "__all__"          
        
class SubjectForm(forms.ModelForm):  
    class Meta:  
        model = Subject  
        fields = "__all__"          
                       
class TimeTableForm(forms.ModelForm):  
    class Meta:  
        model = TimeTable  
        fields = "__all__"          
        
        
        
