from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import PermissionsMixin
from django import forms
from django.utils import timezone



def get_attachment_file_path(instance, filename):
    """
    Produces a unique file path for the upload_to of a FileField.

        The produced path is of the form:
        "[model name]/[field name]/[random name].[filename extension]".
    """

    new_filename = "%s.%s" % (uuid.uuid4(),
                              filename.split('.')[-1])
    return '/'.join([instance.__class__.__name__.lower(),
                      new_filename])



class User(AbstractUser):
    RATING_CHOICES = (
        ('active', 'ACTIVE'),
        ('less_active', 'LESS_ACTIVE'),
        ('independent', 'INDEPENDENT'),

    )
    ROLE_CHOICE=(
        ('supporter', 'SUPPORTER'),
        ('consultant','CONSULTANT'),
    )
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender= models.CharField(choices=GENDER, max_length=10, null=True, blank=True)
    role= models.CharField(choices=ROLE_CHOICE, max_length=15, null=True, blank=True)
    designation=models.CharField(max_length=225,null=True,blank=True)
    employee_id = models.CharField(max_length=20, default=None, null=True)
    skype_username = models.CharField(max_length=50, default=None, null=True)
    mobile_no = models.CharField(max_length=10, null=True, blank=True, )
    company_name = models.CharField(max_length=50, default=None, null=True)
    experience = models.CharField(max_length=5, default=None, null=True)
    status = models.CharField(choices=RATING_CHOICES, max_length=15,null=True, blank=True)
    assigned_date= models.DateField(null=True, blank=True)
    current_location = models.CharField(max_length=30, default=None, null=True)
    resume= models.FileField( upload_to=get_attachment_file_path, default=None, null=True)
    supporter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='consultant')
    log_out_time= models.DateTimeField(null=True,blank=True)

    # def __str__(self):
    #     return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

class Technology(models.Model):
    technology= models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.technology


class Project(models.Model):
    STATUS_CHOICE= (('pending','PENDING'), ('completed','COMPLETED'))
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=2000)
    assigned_date= models.DateField(null=True, blank=True)
    completion_date= models.DateField(null=True, blank=True)
    technology= models.ForeignKey(Technology,null=True, blank=True)
    consultant= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name= 'project')
    status= models.CharField(max_length= 10, choices= STATUS_CHOICE, default= 'pending')
    def __str__(self):
        return self.title

    # def __unicode__(self):
    #    return unicode(self.some_field) or u''
class Comment(models.Model):
    text=models.TextField(max_length=1000, blank=True, null=True)
    comment_time= models.DateTimeField(default=datetime.now)
    project= models.ForeignKey(Project, null=True, blank=True,related_name='comment')
    supporter= models.ForeignKey(User, null=True, blank=True,related_name='comment')
    # reply= models.ForeignKey('self',null=True,blank=True)
    def __str__(self):
        return self.text

class Reply(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='reply')
    reply=models.CharField(max_length=225,null=True,blank=True,)
    reply_time= models.DateTimeField(default=datetime.now)
    supporter= models.ForeignKey(User, null=True, blank=True)

class To_do_list(models.Model):
    text=models.TextField()
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='to_do_list')

    def __str__(self):
        return self.text


class Notification(models.Model):
    text = models.CharField(max_length=225)
    recipient=models.ForeignKey(User,related_name='notification')
    timestamp = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    unread = models.BooleanField(default=True, blank=False)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    send_by= models.ForeignKey(User, null=True,blank=True, related_name='Notification')
    type=models.CharField(null=True,blank=True,max_length=225)

    def __str__(self):
        return self.text


class SkillSet(models.Model):
    technology= models.ForeignKey(Technology,max_length=30, null=True, blank=True)
    pointer= models.IntegerField()
    supporter= models.ForeignKey(User, null=True, blank=True, related_name='skillset',on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.supporter.username