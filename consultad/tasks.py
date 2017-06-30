from __future__ import absolute_import, unicode_literals
# from .celery import app
from celery import Celery, task,shared_task
import os
from celery.schedules import crontab
# from celery import periodic_task
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime

# from celery.task.schedules import crontab
# from celery.decorators import periodic_task


# os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "proj.settings"

logger = get_task_logger(__name__)


app = Celery('tasks', broker='pyamqp://guest@localhost//')

# @app.task
@shared_task
def add(x, y):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
    return (x + y)

def scraper_example(a, b):
     print("###############################")
     return a + b

@periodic_task(run_every=(crontab(minute='*/15')), name="some_task", ignore_result=True)
def scraper_example():
    logger.info("Start task")
    now = datetime.now()
    result = scraper_example(now.day, now.minute)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",result)
    logger.info("Task finished: result = %i" % result)