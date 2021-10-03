from django.db import models
from django.conf import settings


class TodoItemFolder(models.Model):
    """Folders for todo items."""

    name = models.CharField(max_length=256)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class TodoItem(models.Model):
    """A todo item."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    folder = models.ForeignKey(
        TodoItemFolder,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    description = models.TextField()
    done = models.BooleanField()
