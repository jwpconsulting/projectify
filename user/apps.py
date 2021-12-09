"""User apps."""
from django.apps import (
    AppConfig,
)


class UserConfig(AppConfig):
    """UserConfig class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "user"
