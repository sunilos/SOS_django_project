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
        
class College(models.Model):  
    collegeName = models.CharField(max_length=50)  
    collegeAddress = models.CharField(max_length=50)  
    collegeState =  models.CharField(max_length=50)
    collegeCity = models.CharField(max_length=20)  
    collegePhoneNumber=models.CharField(max_length=20)
    class Meta:  
        db_table = "SOS_COLLEGE"          

class Course(models.Model):  
    courseName = models.CharField(max_length=50)  
    courseDescription = models.CharField(max_length=100)  
    courseDuration = models.CharField(max_length=100)  
    class Meta:  
        db_table = "SOS_COURSE"          

class Faculty(models.Model):  
    firstName = models.CharField(max_length=50)  
    lastName = models.CharField(max_length=50)  
    email =  models.EmailField()
    password = models.CharField(max_length=20)
    mobileNumber=models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50) 
    dob = models.DateField(max_length=20) 
    college_ID=models.InetegerField(max_length=50) 
    collegeName = models.CharField(max_length=50) 
    subject_ID=models.InetegerField(max_length=50) 
    subjectName = models.CharField(max_length=50) 
    course_ID=models.InetegerField(max_length=50) 
    courseName = models.CharField(max_length=50)
    class Meta:  
        db_table = "SOS_FACULTY"
          
class Marksheet(models.Model):  
    rollNumber = models.CharField(max_length=50)  
    name = models.CharField(max_length=50)  
    physics=models.InetegerField(max_length=50) 
    chemistry=models.InetegerField(max_length=50) 
    maths=models.InetegerField(max_length=50)
    student_ID=models.InetegerField(max_length=50) 
    class Meta:  
        db_table = "SOS_MARKSHEET"

class student(models.Model):  
    firstName = models.CharField(max_length=50)  
    lastName = models.CharField(max_length=50)  
    dob = models.DateField(max_length=20)
    mobileNumber=models.CharField(max_length=20)
    email =  models.EmailField()
    college_ID=models.InetegerField(max_length=50)
    collegeName = models.CharField(max_length=50)
    class Meta:  
        db_table = "SOS_STUDENT"

class subject(models.Model):  
    subjectName = models.CharField(max_length=50)  
    subjectDescription = models.CharField(max_length=50)  
    dob = models.DateField(max_length=20)
    course_ID=models.InetegerField(max_length=50)
    courseName = models.CharField(max_length=50)
    class Meta:  
        db_table = "SOS_SUBJECT"


class timeTable(models.Model):  
    examTime = models.DateTimeField()
    examDate = models.DateField()
    subject_ID=models.InetegerField(max_length=50) 
    subjectName = models.CharField(max_length=50) 
    course_ID=models.InetegerField(max_length=50) 
    courseName = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    class Meta:  
        db_table = "SOS_TIMETABLE"
