from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import celery
# from settings import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every-10-seconds': {
        'task': 'myapp.views.scheduleT',
        'schedule': 10,
 
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))