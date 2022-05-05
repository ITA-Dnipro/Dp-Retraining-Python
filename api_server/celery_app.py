from celery import Celery

app = Celery(
    "retraining",
    backend="redis://redis/1",
    broker="redis://redis/0",
)

app.autodiscover_tasks()
