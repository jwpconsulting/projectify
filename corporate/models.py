"""Corporate models."""
import uuid

from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    """Customer model. One to one linked to workspace."""

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    workspace = models.OneToOneField(
        "workspace.Workspace",
        on_delete=models.CASCADE,
    )
    seats = models.PositiveIntegerField(default=1)

    class SubscriptionStatus(models.TextChoices):
        """Subscription Choices."""

        ACTIVE = "ACT", _("Active")
        UNPAID = "UNP", _("Unpaid")
        CANCELED = "CAN", _("Canceled")

    subscription_status = models.CharField(
        max_length=3,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.UNPAID,
    )
    stripe_customer_id = models.CharField(
        max_length=150, null=True, blank=True
    )
