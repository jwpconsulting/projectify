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

    ACTIVE = "active"
    UNPAID = "unpaid"
    CANCELLED = "cancelled"


@strawberry.django.type(models.Customer)
class Customer:
    """Customer."""

    @strawberry.field
    def subscription_status(self) -> SubscriptionStatus:
        """Map subscription status."""
        if self.subscription_status == "ACT":
            return SubscriptionStatus.ACTIVE
        elif self.subscription_status == "UNP":
            return SubscriptionStatus.UNPAID
        elif self.subscription_status == "CAN":
            return SubscriptionStatus.CANCELLED
        else:
            raise ValueError(self.subscription_status)

    workspace: workspace_types.Workspace
    seats: int
    uuid: uuid.UUID
