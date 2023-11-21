"""Celery app."""
import configurations
from celery import (
    Celery,
)

configurations.setup()

app = Celery("proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
