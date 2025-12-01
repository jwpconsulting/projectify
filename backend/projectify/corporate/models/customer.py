# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Customer model for corporate app."""

import uuid
from typing import TYPE_CHECKING, ClassVar, Self, cast

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from projectify.corporate.types import CustomerSubscriptionStatus
from projectify.lib.models import BaseModel
from projectify.workspace.models import Workspace


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


class Customer(BaseModel):
    """Customer model. One to one linked to workspace."""

    workspace = models.OneToOneField[Workspace](
        Workspace,
        on_delete=models.CASCADE,
    )
    seats = models.PositiveIntegerField(default=1)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    # TODO track stripe subscription id
    # This can help us prevent double subscriptions
    # TODO track payment method
    # We can show this in the billing UI
    # TODO track last charge succeeded date
    # We can show this in the billing UI
    # TODO track the most recent charge ID
    # We can track this for internal consistency checking
    # TODO track the most recent payment intent ID
    # We can track this for internal consistency checking
    # TODO track when invoices are created, finalized and updated
    # and store their URLs in a related field
    # we can then show the URLs to the invoices in the billing view
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
        # Hm?
        # Justus 2024-02-23
        # unique=True,
        # db_index=True,
    )

    objects: ClassVar[CustomerQuerySet] = cast(  # type: ignore[assignment]
        CustomerQuerySet, CustomerQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        workspace_id: int

    def __str__(self) -> str:
        """Return string representation."""
        return f"Workspace {self.workspace_id} customer"
