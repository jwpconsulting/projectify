"""Todo application config."""
from django.apps import (
    AppConfig,
)


class TodoConfig(AppConfig):
    """TodoConfig class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "todo"
