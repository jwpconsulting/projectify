"""Corporate app config."""
from django.apps import (
    AppConfig,
)
from django.conf import (
    settings,
)

import stripe


class CorporateConfig(AppConfig):
    """App config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "corporate"

    def ready(self) -> None:
        """Execute on loading the app."""
        stripe.api_key = settings.STRIPE_SECRET_KEY
