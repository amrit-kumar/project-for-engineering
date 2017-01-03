from __future__ import unicode_literals
import os, sys
from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import PermissionsMixin
from django import forms
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import PermissionsMixin
from django import forms
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from .validators import validate_file_extension
from django.core.exceptions import ValidationError
from versatileimagefield.fields import VersatileImageField,PPOIField
from PIL import Image
import PIL
from resizeimage import resizeimage








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

# class ImageExampleModel(models.Model):
#     name = models.CharField('Name',max_length=80)
#     image = VersatileImageField('Image',upload_to='images/testimagemodel/',width_field='width',height_field='height')
#     height = models.PositiveIntegerField('Image Height',blank=True,null=True)
#     width = models.PositiveIntegerField('Image Width',blank=True,null=True)
#     image_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

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

    resume= models.FileField( upload_to=get_attachment_file_path, default=None, null=True,validators=[validate_file_extension])
    # image = models.ImageField(upload_to=get_attachment_file_path, null=True, blank=True)
    image = VersatileImageField('Image',upload_to=get_attachment_file_path, ppoi_field='image_ppoi',null=True, blank=True)
    image_ppoi = PPOIField()

    supporter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='consultant')
    log_out_time= models.DateTimeField(null=True,blank=True)



    def __str__(self):
        return 'ID- %s | %s' % (self.id, self.username)


    def save(self, *args, **kwargs):

        # if self.pk is not None:
            # orig = User.objects.get(pk=self.pk)
            # if orig.pk != self.pk:
        super(User, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         hi=Image.open("/home/consultadd/Desktop/workspace/tixdo_space/uttu_project/my_project/consultad/media/__sized__/user/0bc52a0c-6ccd-4f07-a8a4-1a7381ddbb99-kutta-125x125-70.jpg")
    #         print("llllllllllllll",hi.format)
    #         size = 128, 128
    #         print("hi.thumbnail(size)hi.thumbnail(size)",hi.thumbnail(size))
    #         outfile="/home/consultadd/Desktop/projects"
    #         hi.save(outfile, "JPEG")
    #
    #
    #         basewidth = 300
    #         filename = self.get_source_filename()
    #         print("hiiiiiiiiii",filename)
    #         image = Image.open(filename)
    #         wpercent = (basewidth / float(image.size[0]))
    #         hsize = int((float(image.size[1]) * float(wpercent)))
    #         img = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    #         self.image.save()
    #
    #     super(User, self).save(*args, **kwargs)


# class Activity(models.Model):
#     FAVORITE = 'F'
#     LIKE = 'L'
#     UP_VOTE = 'U'
#     DOWN_VOTE = 'D'
#     ACTIVITY_TYPES = (
#         (FAVORITE, 'Favorite'),
#         (LIKE, 'Like'),
#         (UP_VOTE, 'Up Vote'),
#         (DOWN_VOTE, 'Down Vote'),
#     )
#
#     user = models.ForeignKey(User)
#     activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
#     date = models.DateTimeField(auto_now_add=True)
#
#     # Below the mandatory fields for generic relation
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     # content_object = GenericForeignKey()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#     def __str__(self):
#         return 'Object_id- %s | %s' % (self.object_id,self.user.username)

class Technology(models.Model):
    technology= models.CharField(max_length=30)

    def __str__(self):
        return self.technology
        # return 'ID- %s | %s' % (self.id,self.technology)



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
    # activities = GenericRelation(Activity)
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
        # return self.text
        return '%s | ID- %s' % (self.text, self.id)



class SkillSet(models.Model):
    technology= models.ForeignKey(Technology,max_length=30, null=True, blank=True)
    pointer= models.IntegerField()
    supporter= models.ForeignKey(User, null=True, blank=True, related_name='skillset',on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.supporter.username