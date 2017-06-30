from __future__ import absolute_import,unicode_literals

import os
import django

from celery import Celery,task,current_task
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consultad.settings')
django.setup()


app = Celery('consultad')
# app = Celery(
#     'proj', broker='amqp://', backend='amqp://', include=['proj.tasks'])

# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))



# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)