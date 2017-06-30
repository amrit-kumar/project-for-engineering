from __future__ import absolute_import, unicode_literals
# from .celery import app
from celery import Celery, task,shared_task
import os

# from celery.task.schedules import crontab
# from celery.decorators import periodic_task


os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "proj.settings"


app = Celery('tasks', broker='pyamqp://guest@localhost//')

# @app.task
@shared_task
def add(x, y):
    print("##################################################")
    return x + y

# @periodic_task(run_every=(crontab(minute='*/15')), name="some_task", ignore_result=True)
# def some_task()