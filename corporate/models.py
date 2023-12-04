"""Corporate models."""
import uuid
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Self,
    cast,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
    transaction,
)
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from workspace.models import (  # noqa: F401
        Workspace,
    )


class CustomerQuerySet(models.QuerySet["Customer"]):
    """Customer QuerySet."""

    def get_by_uuid(self, uuid: uuid.UUID) -> "Customer":
        """Get Customer by UUID."""
        return self.get(uuid=uuid)

    def get_by_workspace_uuid(self, workspace_uuid: uuid.UUID) -> "Customer":
        """Get workpsace by UUID."""
        return self.get(workspace__uuid=workspace_uuid)

    def filter_by_user(self, user: AbstractBaseUser) -> Self:
        """Filter by user."""
        return self.filter(workspace__users=user)

    def get_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> "Customer":
        """Get customer by user and uuid."""
        return self.filter_by_user(user).get(uuid=uuid)

    def get_by_stripe_customer_id(self, stripe_customer_id: str) -> "Customer":
        """Get customer by stripe customer id."""
        return self.get(stripe_customer_id=stripe_customer_id)


class CustomerSubscriptionStatus(models.TextChoices):
    """Customer subscription status choices."""

    # A subscription has been created with our billing provider
    ACTIVE = "ACTIVE", _("Active")
    # A subscription has never been created with our billing provider
    # TODO this should be "TRIAL"
    UNPAID = "UNPAID", _("Unpaid")
    # An existing subscription with our billing provider has been cancelled
    CANCELLED = "CANCELLED", _("Cancelled")
    # A subscription does not exist, but the workspace can be used without
    # restriction
    CUSTOM = "CUSTOM", _("Custom subscription")


class Customer(models.Model):
    """Customer model. One to one linked to workspace."""

    workspace = models.OneToOneField["Workspace"](
        "workspace.Workspace",
        on_delete=models.CASCADE,
    )
    seats = models.PositiveIntegerField(default=1)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    subscription_status = models.CharField(
        max_length=9,
        choices=CustomerSubscriptionStatus.choices,
        default=CustomerSubscriptionStatus.UNPAID,
    )
    stripe_customer_id = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        # XXX
        # Looks mysterious. Should probably uncomment these:
        # Justus 2023-12-03
        # XXX
        # unique=True,
        # db_index=True,
    )

    objects: ClassVar[CustomerQuerySet] = cast(  # type: ignore[assignment]
        CustomerQuerySet, CustomerQuerySet.as_manager()
    )

    # TODO these four methods should be part of a service
    def activate_subscription(self) -> None:
        """
        Activate customer subscription.

        Saves model instance.
        """
        self.subscription_status = CustomerSubscriptionStatus.ACTIVE
        self.save()

    def cancel_subscription(self) -> None:
        """
        Cancel customer subscription.

        Saves model instance.
        """
        self.subscription_status = CustomerSubscriptionStatus.CANCELLED
        self.save()

    def assign_stripe_customer_id(self, stripe_customer_id: str) -> None:
        """
        Assign stripe customer id.

        Saves model instance.
        """
        self.stripe_customer_id = stripe_customer_id
        self.save()

    def set_number_of_seats(self, seats: int) -> None:
        """
        Set the number of seats.

        Saves model instance.
        """
        if self.seats == seats:
            return None
        self.seats = seats
        self.save()

    # TODO this should be a selector.
    # XXX this prop can have an n+1 as a side effect
    @property
    @transaction.atomic
    def seats_remaining(self) -> int:
        """Return the number of seats remaining."""
        num_users = len(self.workspace.users.all())
        invites_qs = self.workspace.workspaceuserinvite_set.all()
        num_invites = len(invites_qs)
        return self.seats - num_users - num_invites
