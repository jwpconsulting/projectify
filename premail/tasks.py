"""Premail tasks."""
from django.conf import (
    settings,
)
from django.core import (
    mail,
)

from projectify.celery import (
    app,
)


# TODO turn into shared_task
@app.task()
def send_mail(subject: str, body: str, to_email: str) -> None:
    """Send an email."""
    mail.send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
    )
