import os

from celery import Celery

app = Celery(
    "retraining",
    backend=os.environ.get('RESULT_BACKEND'),
    broker=os.environ.get('BROKER_URL'),
)

app.autodiscover_tasks()
