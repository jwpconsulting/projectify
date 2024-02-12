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
"""Test customer model in corporate app."""
from unittest import mock

import pytest

from corporate.models import Customer
from corporate.services.customer import (
    customer_activate_subscription,
    customer_cancel_subscription,
    customer_check_active_for_workspace,
    customer_update_seats,
)
from workspace.models.workspace import Workspace


@pytest.mark.django_db
def test_subscription_activation(
    unpaid_customer: Customer,
    workspace: Workspace,
    stripe_customer_id: str,
) -> None:
    """Test activating subscription."""
    assert customer_check_active_for_workspace(workspace=workspace) == "trial"
    customer_activate_subscription(
        customer=unpaid_customer, stripe_customer_id=stripe_customer_id
    )
    unpaid_customer.refresh_from_db()
    assert customer_check_active_for_workspace(workspace=workspace) == "full"


@pytest.mark.django_db
def test_cancel_subscription(
    workspace: Workspace, paid_customer: Customer
) -> None:
    """Test cancel_subscription will revert a workspace to trial."""
    assert customer_check_active_for_workspace(workspace=workspace)
    customer_cancel_subscription(customer=paid_customer)
    paid_customer.refresh_from_db()
    assert customer_check_active_for_workspace(workspace=workspace) == "trial"


@pytest.mark.django_db
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
        customer=unpaid_customer, stripe_customer_id=stripe_customer_id
    )
    assert customer_check_active_for_workspace(workspace=workspace) == "full"
