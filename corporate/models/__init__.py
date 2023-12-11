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

from corporate.types import CustomerSubscriptionStatus

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


# TODO use BaseModel
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
