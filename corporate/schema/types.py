"""Corporate schema types."""
import enum
import uuid

import strawberry

from workspace.schema import types as workspace_types

from .. import (
    models,
)


@strawberry.enum
class SubscriptionStatus(enum.Enum):
    """Subscription status enum."""

    ACTIVE = "ACTIVE"
    UNPAID = "UNPAID"
    CANCELLED = "CANCELLED"


@strawberry.django.type(models.Customer)
class Customer:
    """Customer."""

    @strawberry.field
    def subscription_status(self) -> SubscriptionStatus:
        """Map subscription status."""
        if self.subscription_status == "ACTIVE":
            return SubscriptionStatus.ACTIVE
        elif self.subscription_status == "UNPAID":
            return SubscriptionStatus.UNPAID
        elif self.subscription_status == "CANCELLED":
            return SubscriptionStatus.CANCELLED
        else:
            raise ValueError(self.subscription_status)

    workspace: workspace_types.Workspace
    seats: int
    seats_remaining: int
    uuid: uuid.UUID


@strawberry.type
class CheckoutSession:
    """Checkout session."""

    @strawberry.field
    def stripe_id(self) -> str:
        """Return stripe id."""
        return self.id

    url: str


@strawberry.type
class BillingPortalSession:
    """Billing portal session."""

    url: str
