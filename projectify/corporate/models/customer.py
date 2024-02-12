# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Customer model for corporate app."""
import uuid
from typing import (
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
from projectify.lib.models import BaseModel
from workspace.models import Workspace


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
