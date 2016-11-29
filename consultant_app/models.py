from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import PermissionsMixin
from django import forms



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
    employee_id = models.CharField(max_length=20, default=None, null=True)
    skype_username = models.CharField(max_length=50, default=None, null=True)
    mobile_no = models.CharField(max_length=10, null=True, blank=True, )
    company_name = models.CharField(max_length=50, default=None, null=True)
    experience = models.CharField(max_length=5, default=None, null=True)
    status = models.CharField(choices=RATING_CHOICES, max_length=15, null=True, blank=True)

    current_location = models.CharField(max_length=30, default=None, null=True)
    resume= models.FileField( upload_to=get_attachment_file_path, default=None, null=True)

    supporter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='consultant')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)


class Project(models.Model):
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=2000)
    assigned_date= models.DateField(null=True, blank=True)
    completion_date= models.DateField(null=True, blank=True)
    technology= models.CharField(max_length=20, null=True, blank=True)
    consultant= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name= 'project')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text=models.TextField(max_length=1000, blank=True, null=True)
    comment_time= models.DateTimeField(default=datetime.now)
    project= models.ForeignKey(Project, null=True, blank=True)
    supporter= models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.text


