from symbol import test

from celery import Celery
from celery.schedules import crontab
app = Celery()

from celery import task
from celery.task import periodic_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
@periodic_task(run_every=crontab(minute="0", hour="23"))
def do_every_midnight():
    print("hiiiiii  celery")
 #your code

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )