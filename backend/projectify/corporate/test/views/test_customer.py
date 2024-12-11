# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test customer views."""

from collections.abc import Iterable
from unittest import mock

from django.urls import reverse

import pytest
from faker import Faker
from rest_framework.test import APIClient

from projectify.settings.base import Base
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from pytest_types import DjangoAssertNumQueries

from ...models import Customer

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def patch_stripe_settings(
    settings: Base,
    stripe_price_object: str,
    stripe_secret_key: str,
    stripe_endpoint_secret: str,
) -> None:
    """Patch stripe settings."""
    settings.STRIPE_SECRET_KEY = stripe_secret_key
    settings.STRIPE_ENDPOINT_SECRET = stripe_endpoint_secret
    settings.STRIPE_PRICE_OBJECT = stripe_price_object


# Read
class TestWorkspaceCustomerRetrieve:
    """Test WorkspaceCustomerRetrieve."""

    @pytest.fixture
    def resource_url(self, paid_customer: Customer) -> str:
        """Return URL to resource."""
        return reverse(
            "corporate:customers:read", args=(paid_customer.workspace.uuid,)
        )

    def test_authenticated(
        self,
        user_client: APIClient,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test as authenticated user."""
        with django_assert_num_queries(4):
            response = user_client.get(resource_url)
            assert response.status_code == 200, response.content

    def test_404(
        self,
        rest_meddling_client: APIClient,
        resource_url: str,
    ) -> None:
        """Test no workspace/customer locatable for current user."""
        response = rest_meddling_client.get(resource_url)
        assert response.status_code == 404, response.content


# RPC
class MockSession:
    """Checkout and billing portal mock session."""

    url = "https://www.example.com"


class TestWorkspaceCheckoutSessionCreate:
    """Test creating a checkout session."""

    @pytest.fixture(autouse=True)
    def mock_stripe_checkout(
        self,
    ) -> Iterable[mock.MagicMock]:
        """Mock stripe checkout session creation."""
        with mock.patch(
            "stripe.checkout._session_service.SessionService.create"
        ) as m:
            m.return_value = MockSession()
            yield m

    def test_invalid_uuid(
        self,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        faker: Faker,
    ) -> None:
        """Test passing in an invalid uuid."""
        resource_url = reverse(
            "corporate:customers:create-checkout-session",
            args=(str(faker.uuid4()),),
        )
        with django_assert_num_queries(1):
            response = rest_user_client.post(
                resource_url, data={"seats": 1337}
            )
            assert response.status_code == 404, response.data

    def test_posting_normal_data(
        self,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        unpaid_customer: Customer,
    ) -> None:
        """Test we can get a url when posting valid data."""
        resource_url = reverse(
            "corporate:customers:create-checkout-session",
            args=(str(unpaid_customer.workspace.uuid),),
        )
        with django_assert_num_queries(7):
            response = rest_user_client.post(
                resource_url,
                data={"seats": 1337},
            )
            assert response.status_code == 200, response.data
        assert response.data == {"url": "https://www.example.com"}

    @pytest.mark.xfail(
        reason="Test is redundant, customers are always created"
    )
    def test_no_customer(
        self,
        mock_stripe_checkout: mock.MagicMock,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        team_member: TeamMember,
        workspace: Workspace,
    ) -> None:
        """Test it works even with no customer."""
        del mock_stripe_checkout
        resource_url = reverse(
            "corporate:customers:create-checkout-session",
            args=(str(workspace.uuid),),
        )
        # More queries since we create a customer here
        with django_assert_num_queries(8):
            response = rest_user_client.post(
                resource_url,
                data={"seats": 1337},
            )
            assert response.status_code == 200, response.data
        assert response.data == {"url": "https://www.example.com"}

    def test_paid_customer(
        self,
        mock_stripe_checkout: mock.MagicMock,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        paid_customer: Customer,
    ) -> None:
        """Test that there is an error on paid customer."""
        del mock_stripe_checkout
        resource_url = reverse(
            "corporate:customers:create-checkout-session",
            args=(str(paid_customer.workspace.uuid),),
        )
        with django_assert_num_queries(6):
            response = rest_user_client.post(
                resource_url,
                data={"seats": 1337},
            )
            assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {},
            "general": "This customer already activated a subscription before",
        }


class TestWorkspaceBillingPortalSessionCreate:
    """Test creating billing portal sessions."""

    @pytest.fixture(autouse=True)
    def mock_stripe_billing_portal(self) -> Iterable[mock.MagicMock]:
        """Mock stripe billing portal session creation."""
        with mock.patch(
            "stripe.billing_portal._session_service.SessionService.create"
        ) as m:
            m.return_value = MockSession()
            yield m

    def test_with_unpaid_customer(
        self,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        unpaid_customer: Customer,
    ) -> None:
        """Assert that an unpaid customer cannot access this view."""
        resource_url = reverse(
            "corporate:customers:create-billing-portal-session",
            args=(str(unpaid_customer.workspace.uuid),),
        )
        with django_assert_num_queries(3):
            response = rest_user_client.post(resource_url)
            assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {},
            "general": "Can not create billing portal session because no subscription is active. If you believe this is an error, please contact support.",
        }

    def test_with_paying_customer(
        self,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        paid_customer: Customer,
    ) -> None:
        """Test calling this with a paying customer."""
        resource_url = reverse(
            "corporate:customers:create-billing-portal-session",
            args=(str(paid_customer.workspace.uuid),),
        )
        with django_assert_num_queries(3):
            response = rest_user_client.post(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == {"url": "https://www.example.com"}
