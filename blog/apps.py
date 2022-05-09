"""Blogs apps.py."""
from django.apps import (
    AppConfig,
)


class BlogConfig(AppConfig):
    """Blog apps.py config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
