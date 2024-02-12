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
"""Test coupon views."""
from django.urls import reverse

import pytest
from rest_framework.test import APIClient

from corporate.models.coupon import Coupon
from corporate.models.customer import Customer
from corporate.services.customer import customer_check_active_for_workspace
from pytest_types import DjangoAssertNumQueries
from workspace.models.workspace import Workspace


@pytest.mark.django_db
class TestCouponRedeem:
    """Test redeeming coupons."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "corporate:coupons:redeem-coupon",
            args=(str(workspace.uuid),),
        )

    def test_redeeming_invalid_code(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
    ) -> None:
        """Test that nothing bad happens with an invalid code."""
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "trial"
        )
        with django_assert_num_queries(8):
            response = rest_user_client.post(
                resource_url,
                data={"code": "thiscodedoesnotexist"},
            )
            assert response.status_code == 400, response.data
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "trial"
        )

    def test_redeeming_valid_code(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        coupon: Coupon,
        workspace: Workspace,
        unpaid_customer: Customer,
    ) -> None:
        """Test that workspace subscription is actived correctly."""
        assert unpaid_customer.seats != 20
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "trial"
        )
        with django_assert_num_queries(9):
            response = rest_user_client.post(
                resource_url,
                data={"code": coupon.code},
            )
            assert response.status_code == 204, response.data

        unpaid_customer.refresh_from_db()
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "full"
        )
        # Taken from seats in conftest.py
        assert unpaid_customer.seats == 20
