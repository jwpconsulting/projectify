# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Test stripe services in corporate app."""
from unittest import mock

import pytest
from rest_framework.exceptions import PermissionDenied

from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace

from ...models import Customer
from ...selectors.customer import (
    customer_check_active_for_workspace,
)
from ...services.customer import (
    create_billing_portal_session_for_customer,
)
from ...services.stripe import (
    customer_activate_subscription,
    customer_cancel_subscription,
    customer_update_seats,
)

pytestmark = pytest.mark.django_db


class TestCreateBillingPortalSessionForWorkspaceUuid:
    """Test create_billing_portal_session_for_workspace_uuid."""

    def test_missing_customer_id(
        self, team_member: TeamMember, unpaid_customer: Customer
    ) -> None:
        """Test missing customer id will throw ValueError."""
        with pytest.raises(PermissionDenied) as error:
            create_billing_portal_session_for_customer(
                customer=unpaid_customer, who=team_member.user
            )
        assert error.match("no subscription is active")


def test_subscription_activation(
    unpaid_customer: Customer,
    workspace: Workspace,
    stripe_customer_id: str,
) -> None:
    """Test activating subscription."""
    assert customer_check_active_for_workspace(workspace=workspace) == "trial"
    customer_activate_subscription(
        customer=unpaid_customer,
        stripe_customer_id=stripe_customer_id,
        seats=1337,
    )
    unpaid_customer.refresh_from_db()
    assert customer_check_active_for_workspace(workspace=workspace) == "full"
    assert unpaid_customer.seats == 1337


def test_cancel_subscription(
    workspace: Workspace, paid_customer: Customer
) -> None:
    """Test cancel_subscription will revert a workspace to trial."""
    assert customer_check_active_for_workspace(workspace=workspace)
    customer_cancel_subscription(customer=paid_customer)
    paid_customer.refresh_from_db()
    assert customer_check_active_for_workspace(workspace=workspace) == "trial"


def test_set_number_of_seats(unpaid_customer: Customer) -> None:
    """Test set_number_of_seats."""
    original_seats = unpaid_customer.seats
    customer_update_seats(customer=unpaid_customer, seats=original_seats + 1)
    unpaid_customer.refresh_from_db()
    assert unpaid_customer.seats == original_seats + 1

    # TODO
    # We are testing whether the db is not hit - but what does it achieve?
    save_mock = mock.MagicMock()
    unpaid_customer.save = save_mock  # type: ignore
    customer_update_seats(customer=unpaid_customer, seats=original_seats + 1)
    assert not save_mock.called


@pytest.mark.django_db
def test_active(
    stripe_customer_id: str, workspace: Workspace, unpaid_customer: Customer
) -> None:
    """Test active property."""
    assert customer_check_active_for_workspace(workspace=workspace) == "trial"
    customer_activate_subscription(
        customer=unpaid_customer,
        stripe_customer_id=stripe_customer_id,
        seats=1337,
    )
    assert customer_check_active_for_workspace(workspace=workspace) == "full"
