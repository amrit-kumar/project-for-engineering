
from __future__ import absolute_import

from celery import shared_task,task
from .models import *

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@task
def create_user(username, password):
    User.objects.create(username=username, password=password)