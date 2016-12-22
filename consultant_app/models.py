from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import PermissionsMixin
from django import forms
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType




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


    def __str__(self):
        return 'ID- %s | %s' % (self.id, self.username)

    # def __str__(self):
    #     return self.username
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

class Technology(models.Model):
    technology= models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return 'ID- %s | %s' % (self.id,self.technology)

class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'Object_id- %s | %s' % (self.object_id,self.user.username)


class Project(models.Model):
    STATUS_CHOICE= (('pending','PENDING'), ('completed','COMPLETED'))
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=2000)
    assigned_date= models.DateField(null=True, blank=True)
    completion_date= models.DateField(null=True, blank=True)
    technology= models.ForeignKey(Technology,max_length=20, null=True, blank=True)
    consultant= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name= 'project')
    status= models.CharField(max_length= 10, choices= STATUS_CHOICE, default= 'pending')

    # def __str__(self):
    #     return self.title
    def __str__(self):
        return 'ID- %s | %s' % (self.id,self.title)

# class Like(models.Model):
#     user = models.ForeignKey(User, related_name='likess',null=True, blank=True)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,related_name='content')
#     object_id = models.PositiveIntegerField(default=5)
#     content_object = GenericForeignKey('content_type', 'object_id')

class Comment(models.Model):
    text=models.TextField(max_length=1000, blank=True, null=True)
    comment_time= models.DateTimeField(default=datetime.now)
    project= models.ForeignKey(Project, null=True, blank=True,related_name='comment')
    supporter= models.ForeignKey(User, null=True, blank=True,related_name='comment')
    activities = GenericRelation(Activity)


    # likes = GenericRelation(Like)
    def __str__(self):
        return self.text

class Reply(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='reply')
    reply=models.CharField(max_length=225,null=True,blank=True,)
    reply_time= models.DateTimeField(default=datetime.now)
    supporter= models.ForeignKey(User, null=True, blank=True)

class To_do_list(models.Model):
    # text=ArrayField(models.CharField(max_length=200), blank=True)
    text=models.CharField(max_length=200, blank=True)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='to_do_list')

    # def __str__(self):
    #     return self.pk



class Notification(models.Model):
    text = models.CharField(max_length=225)
    recipient=models.ForeignKey(User,related_name='notification')
    timestamp = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    unread = models.BooleanField(default=True, blank=False)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    sender=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='Notification')

    def __str__(self):
        return self.text


class SkillSet(models.Model):
    technology= models.ForeignKey(Technology,max_length=30, null=True, blank=True)
    pointer= models.IntegerField()
    supporter= models.ForeignKey(User, null=True, blank=True, related_name='skillset',on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.supporter.username




