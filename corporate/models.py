"""Corporate models."""
import uuid

from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _


class CustomerManager(models.Manager):
    """Custom Manager for Customer model."""

    def get_by_uuid(self, uuid):
        """Get Customer by UUID."""
        return self.get(uuid=uuid)


class Customer(models.Model):
    """Customer model. One to one linked to workspace."""

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    workspace = models.OneToOneField(
        "workspace.Workspace",
        on_delete=models.CASCADE,
    )
    seats = models.PositiveIntegerField(default=1)

    objects = CustomerManager()

    class SubscriptionStatus(models.TextChoices):
        """Subscription Choices."""

        ACTIVE = "ACT", _("Active")
        UNPAID = "UNP", _("Unpaid")
        CANCELLED = "CAN", _("Cancelled")

    subscription_status = models.CharField(
        max_length=3,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.UNPAID,
    )
    stripe_customer_id = models.CharField(
        max_length=150, null=True, blank=True
    )

    def activate_subscription(self):
        """
        Activate customer subscription.

        Saves model instance.
        """
        self.subscription_status = Customer.SubscriptionStatus.ACTIVE
        self.save()

    def cancel_subscription(self):
        """
        Cancel customer subscription.

        Saves model instance.
        """
        self.subscription_status = Customer.SubscriptionStatus.CANCELLED
        self.save()

    def assign_stripe_customer_id(self, stripe_customer_id):
        """
        Assign stripe customer id.

        Saves model instance.
        """
        self.stripe_customer_id = stripe_customer_id
        self.save()

    @property
    def active(self):
        """Return if active customer."""
        return self.subscription_status == Customer.SubscriptionStatus.ACTIVE
