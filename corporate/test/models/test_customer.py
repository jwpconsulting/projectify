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
"""Test corporate models."""

import pytest
from faker import Faker

from corporate.models import Customer
from user.models import User
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
)


@pytest.mark.django_db
class TestCustomerManager:
    """Test Customer Manager."""

    def test_get_by_uuid(self, unpaid_customer: Customer) -> None:
        """Test get Customer by UUID."""
        customer_by_manager = Customer.objects.get_by_uuid(
            unpaid_customer.uuid
        )
        assert unpaid_customer == customer_by_manager

    def test_get_by_workspace_uuid(self, unpaid_customer: Customer) -> None:
        """Test get_by_workspace_uuid."""
        assert (
            Customer.objects.get_by_workspace_uuid(
                unpaid_customer.workspace.uuid
            )
            == unpaid_customer
        )

    def test_filter_by_user(
        self,
        unpaid_customer: Customer,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test filter_by_user."""
        qs = Customer.objects.filter_by_user(workspace_user.user)
        assert list(qs) == [unpaid_customer]

    def test_get_for_user_and_uuid(
        self,
        unpaid_customer: Customer,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test get_for_user_and_uuid."""
        assert (
            Customer.objects.get_for_user_and_uuid(
                workspace_user.user, unpaid_customer.uuid
            )
            == unpaid_customer
        )

    def test_get_by_stripe_customer_id(
        self, unpaid_customer: Customer
    ) -> None:
        """Test get_by_stripe_customer_id."""
        unpaid_customer.stripe_customer_id = "hello_world"
        unpaid_customer.save()
        assert (
            Customer.objects.get_by_stripe_customer_id(
                "hello_world",
            )
            == unpaid_customer
        )


@pytest.mark.django_db
class TestCustomer:
    """Test customer model."""

    def test_factory(self, unpaid_customer: Customer) -> None:
        """Test factory."""
        assert unpaid_customer.workspace

    def test_seats_remaining(
        self,
        paid_customer: Customer,
        faker: Faker,
        user: User,
    ) -> None:
        """Test seats remaining."""
        # user is already added, so there is already one seat used up
        assert paid_customer.seats_remaining == paid_customer.seats - 1
        add_or_invite_workspace_user(
            who=user,
            workspace=paid_customer.workspace,
            email_or_user=faker.email(),
        )
        assert paid_customer.seats_remaining == paid_customer.seats - 2
