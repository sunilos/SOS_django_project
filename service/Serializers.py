from rest_framework import serializers
from .models import User, Role,College,Course,Faculty,Marksheet,Student,Subject,TimeTable

        
class CollegeSerializers(serializers.ModelSerializer):  
    class Meta:  
        model = College  
        fields = "__all__"          

