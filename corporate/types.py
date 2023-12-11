"""Corporate app types."""
from typing import Literal

from django.db import models
from django.utils.translation import gettext_lazy as _

WorkspaceFeatures = Literal["full", "trial", "inactive"]


class CustomerSubscriptionStatus(models.TextChoices):
    """Customer subscription status choices."""

    # A subscription has been created with our billing provider
    ACTIVE = "ACTIVE", _("Active")
    # A subscription has never been created with our billing provider
    # TODO this should be "TRIAL" or similar
    UNPAID = "UNPAID", _("Unpaid")
    # An existing subscription with our billing provider has been cancelled
    CANCELLED = "CANCELLED", _("Cancelled")
    # A subscription does not exist, but the workspace can be used without
    # restriction
    CUSTOM = "CUSTOM", _("Custom subscription")
