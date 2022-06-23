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

    def get_by_workspace_uuid(self, workspace_uuid):
        """Get workpsace by UUID."""
        return self.get(workspace__uuid=workspace_uuid)

    def get_for_user_and_uuid(self, user, uuid):
        """Get customer by user and uuid."""
        return self.filter(workspace__users=user).get(uuid=uuid)

    def get_by_stripe_customer_id(self, stripe_customer_id):
        """Get customer by stripe customer id."""
        return self.get(stripe_customer_id=stripe_customer_id)


class Customer(models.Model):
    """Customer model. One to one linked to workspace."""

    class SubscriptionStatus(models.TextChoices):
        """Subscription Choices."""

        ACTIVE = "ACT", _("Active")
        UNPAID = "UNP", _("Unpaid")
        CANCELLED = "CAN", _("Cancelled")

    workspace = models.OneToOneField(
        "workspace.Workspace",
        on_delete=models.CASCADE,
    )
    seats = models.PositiveIntegerField(default=1)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    subscription_status = models.CharField(
        max_length=3,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.UNPAID,
    )
    stripe_customer_id = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        # XXX
        # unique=True,
        # db_index=True,
    )

    objects = CustomerManager()

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

    def set_number_of_seats(self, seats):
        """
        Set the number of seats.

        Saves model instance.
        """
        if self.seats == seats:
            return
        self.seats = seats
        self.save()

    @property
    def active(self):
        """Return if active customer."""
        return self.subscription_status == Customer.SubscriptionStatus.ACTIVE
