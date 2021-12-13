"""Celery app."""
from celery import (
    Celery,
)


app = Celery("proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
