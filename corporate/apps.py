"""Corporate app config."""
from django.apps import (
    AppConfig,
)


class CorporateConfig(AppConfig):
    """App config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "corporate"
