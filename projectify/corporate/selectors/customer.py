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
from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace

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
        workspace = Workspace.objects.filter_for_user_and_uuid(
            user=who,
            uuid=workspace_uuid,
        ).get()
    except Workspace.DoesNotExist:
        logger.warning("No workspace found for uuid %s", workspace_uuid)
        return None
    try:
        return workspace.customer
    except Customer.DoesNotExist:
        return None
