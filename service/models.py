from django.db import models

# Create your models here.
class Role(models.Model):  
    name = models.CharField(max_length=100)  
    description =  models.CharField(max_length=500)
    class Meta:  
        db_table = "SOS_ROLE"  

class User(models.Model):  
    firstName = models.CharField(max_length=50)  
    lastName = models.CharField(max_length=50)  
    login =  models.EmailField()
    password = models.CharField(max_length=20)  

    class Meta:  
        db_table = "SOS_USER"          