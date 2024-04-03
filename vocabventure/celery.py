import os
from vocabventure.celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vocabventure.settings')

app = Celery('vocabventure')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()