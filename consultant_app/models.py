from __future__ import unicode_literals
from django.conf import settings
from datetime import datetime
from django.utils import timezone

from django.db import models

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

STATUS = (
    ('active', 'active'),
    ('less_active', 'less_active'),
    ('independent', 'independent'),

)

class Project(models.Model):
    project_title=models.CharField(max_length=100,blank=True,null=True)
    project_description=models.TextField(max_length=1000)
    assigned_date=models.DateTimeField(default=datetime.now())
    completion_date=models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.project_title


class Supporter(models.Model):
    user=models.OneToOneField(USER_MODEL)
    email= models.EmailField(max_length=255, blank=True, null=True)
    skype_username=models.CharField(max_length=100, blank=True, null=True)
    mobile_no= models.IntegerField(max_length=25, blank=True, null=True)


    def __str__(self):
        return str(self.id)


# Create your models here.
class Consultant(models.Model):
    user = models.OneToOneField(USER_MODEL)
    recruiter  = models.ForeignKey(USER_MODEL, related_name="recruits", blank=True, null=True)
    email= models.EmailField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=15,choices=STATUS)
    skype_username=models.CharField(max_length=100, blank=True, null=True)
    mobile_no= models.IntegerField(max_length=25, blank=True, null=True)
    company_name=models.CharField(max_length=100, null=True,blank=True)
    project_id=models.OneToOneField(Project,on_delete=models.CASCADE)
    experience=models.CharField(max_length=20,blank=True,null=True)
    curr_loc = models.CharField(max_length=100, blank=True, null=True)
    supporter_id=models.ForeignKey(Supporter,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    comment=models.CharField(max_length=500)
    created_time=models.DateTimeField(default=datetime.now())
    project_id=models.ForeignKey(Project,on_delete=models.CASCADE)
    supporter_id=models.ForeignKey(Supporter,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
