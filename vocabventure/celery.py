from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, signals
from celery import shared_task
import logging

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vocabventure.settings')

app = Celery('vocabventure')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = logging.getLogger('celery')

app.conf.broker_url = os.environ.get('CELERY_BROKER_URL')

@signals.task_prerun.connect
def task_prerun_handler(*args, **kwargs):
    task = kwargs.get('sender')
    task_id = kwargs.get('task_id')
    logger.info(f"Task {task.name} [{task_id}] is about to run.")