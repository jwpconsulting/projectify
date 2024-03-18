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

from projectify.corporate.models import Customer
from projectify.workspace.models.team_member import TeamMember


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
        team_member: TeamMember,
    ) -> None:
        """Test filter_by_user."""
        qs = Customer.objects.filter_by_user(team_member.user)
        assert list(qs) == [unpaid_customer]

    def test_get_for_user_and_uuid(
        self,
        unpaid_customer: Customer,
        team_member: TeamMember,
    ) -> None:
        """Test get_for_user_and_uuid."""
        assert (
            Customer.objects.get_for_user_and_uuid(
                team_member.user, unpaid_customer.uuid
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
