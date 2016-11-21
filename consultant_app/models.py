from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser



class UserProfile(AbstractUser):

    Role_choice = (
        ('consultant', 'CONSULTANT'),
        ('supporter', 'SUPPORTER'),
        # ('recruiter', 'RECRUITER'),
        # ('no_role', 'NO_ROLE')

    )
    role= models.CharField(max_length=20, choices=Role_choice, default='NO_ROLE')
    def __str__(self):
        return self.username


class Project(models.Model):
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=2000)
    assigned_date= models.DateField(null=True, blank=True)
    completion_date= models.DateField(null=True, blank=True)
    # assigned_date=models.DateTimeField(null=True, blank=True)
    # completion_date=models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title

class Supporter(models.Model):
    # username= models.CharField(max_length=30,)

    employee_id= models.CharField(max_length=20, null=True, blank=True)
    supporter = models.OneToOneField(UserProfile)
    # username = models.CharField(max_length=30, default=supporter.username )
    skype_username = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)

    def __str__(self):
        return '%s %s' % (self.employee_id, self.supporter.username)
class Consultant(models.Model):
    RATING_CHOICES = (
        ('active', 'ACTIVE'),
        ('less_active', 'LESS_ACTIVE'),
        ('independent', 'INDEPENDENT'),

    )
    # username= models.CharField(max_length=30, null=True, blank=True)

    consultant = models.OneToOneField(UserProfile)
    employee_id= models.CharField(max_length=20, null=True, blank=True)
    skype_username= models.CharField(max_length=50)
    mobile_no= models.CharField(max_length=10)
    company_name= models.CharField(max_length=50)
    experience= models.CharField(max_length=5, null=True, blank=True)
    status= models.CharField(choices=RATING_CHOICES, max_length=15)
    current_location=models.CharField(max_length=30)
    supporter = models.ForeignKey(Supporter,related_name="consultant", on_delete=models.CASCADE)
    shadow_supporter= models.ForeignKey(Supporter, related_name="shadow_supporter", on_delete=models.CASCADE, null=True, blank=True)
    project= models.ForeignKey(Project,related_name="projects", on_delete=models.CASCADE)
    # username = models.CharField(max_length=30, default=consultant.username )



    def __str__(self):
        return '%s %s' % (self.employee_id, self.consultant.username)

class Comment(models.Model):
    text=models.TextField(max_length=1000, blank=True, null=True)
    comment_time= models.DateTimeField(default=datetime.now)
    project= models.ForeignKey(Project, null=True, blank=True)
    supporter= models.ForeignKey(Supporter, null=True, blank=True)

    def __str__(self):
        return self.title


