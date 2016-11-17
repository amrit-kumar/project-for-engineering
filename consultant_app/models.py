from django.db import models
from django.conf import settings
from datetime import datetime

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')




class Project(models.Model):
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=2000)
    assigned_date= models.DateField
    completion_date= models.DateField

    def __str__(self):
        return self.title

class Supporter(models.Model):
    user = models.OneToOneField(USER_MODEL)
    skype_username = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Consultant(models.Model):
    RATING_CHOICES = (
        ('active', 'ACTIVE'),
        ('less_active', 'LESS_ACTIVE'),
        ('independent', 'INDEPENDENT'),

    )
    user = models.OneToOneField(USER_MODEL)
    skype_username= models.CharField(max_length=50)
    mobile_no= models.CharField(max_length=10)
    company_name= models.CharField(max_length=50)
    experience= models.CharField(max_length=5, null=True, blank=True)
    status= models.CharField(choices=RATING_CHOICES, max_length=15)
    current_location=models.CharField(max_length=30)
    recruiter = models.ForeignKey(USER_MODEL, related_name="recruits", blank=True, null=True)
    supporter_id = models.ForeignKey(Supporter, on_delete=models.CASCADE)
    project_id= models.OneToOneField(Project, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

class Comment(models.Model):
    title=models.CharField(max_length=100,blank=True,null=True)
    description=models.TextField(max_length=1000, blank=True, null=True)
    assigned_date=models.DateTimeField(default=datetime.now())
    completion_date=models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title
