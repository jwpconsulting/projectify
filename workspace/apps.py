"""Workspace app configs."""
from django.apps import (
    AppConfig,
)


class WorkspaceConfig(AppConfig):
    """Workspace AppConfig."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "workspace"
