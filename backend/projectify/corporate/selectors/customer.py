# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Corporate app customer model selectors."""

import logging
from typing import Optional
from uuid import UUID

from projectify.corporate.models import Customer
from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace

from ..types import (
    CustomerSubscriptionStatus,
    WorkspaceFeatures,
)

logger = logging.getLogger(__name__)


# Does not perform permission checking, this is needed for stripe
# TODO optionally consider if we should add permission checking here?
# Can this accidentally be used in a regular customer facing view?
def customer_find_by_uuid(*, customer_uuid: UUID) -> Optional[Customer]:
    """Find a customer by UUID."""
    try:
        # The following method can be refactored in here
        return Customer.objects.get_by_uuid(customer_uuid)
    except Customer.DoesNotExist:
        return None


# Does not perform permission checking, this is needed for stripe
def customer_find_by_stripe_customer_id(
    *, stripe_customer_id: str
) -> Optional[Customer]:
    """Find a customer by stripe id."""
    try:
        # The following method can be refactored in here
        return Customer.objects.get_by_stripe_customer_id(stripe_customer_id)
    except Customer.DoesNotExist:
        return None


def customer_find_by_workspace_uuid(
    *,
    workspace_uuid: UUID,
    who: User,
) -> Optional[Customer]:
    """Find a customer given a workspace uuid."""
    try:
        customer = Customer.objects.select_related("workspace").get(
            workspace__uuid=workspace_uuid,
            workspace__users=who,
        )
    except Customer.DoesNotExist:
        logger.error("No customer found for uuid %s. Why?", workspace_uuid)
        return None

    validate_perm("corporate.can_read_customer", who, customer.workspace)
    return customer


# TODO permissions needed?
# TODO check whether a workspace is in trial, then check further conditions
# TODO rename customer_check_workspace_features
def customer_check_active_for_workspace(
    *, workspace: Workspace
) -> WorkspaceFeatures:
    """Check if a customer is active for a given workspace."""
    try:
        customer = workspace.customer
    except Customer.DoesNotExist:
        raise ValueError(f"No customer found for workspace {workspace}")
    match customer.subscription_status:
        case CustomerSubscriptionStatus.ACTIVE:
            return "full"
        case CustomerSubscriptionStatus.CUSTOM:
            return "full"
        case CustomerSubscriptionStatus.UNPAID:
            return "trial"
        case CustomerSubscriptionStatus.CANCELLED:
            return "trial"
        case status:
            raise ValueError(f"Unknown status {status}")
