# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test coupon views."""

from django.urls import reverse

import pytest
from rest_framework.test import APIClient

from projectify.workspace.models.workspace import Workspace
from pytest_types import DjangoAssertNumQueries

from ...models.coupon import Coupon
from ...models.customer import Customer
from ...selectors.customer import customer_check_active_for_workspace


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
        with django_assert_num_queries(7):
            response = rest_user_client.post(
                resource_url,
                data={"code": "thiscodedoesnotexist"},
            )
            assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {"code": "No coupon is available for this code"},
            "general": None,
        }
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
        with django_assert_num_queries(8):
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
