"""Test customer views."""
from collections.abc import Iterable
from unittest import mock

from django.conf import LazySettings
from django.urls import (
    reverse,
)

import pytest
from faker import Faker
from rest_framework.test import APIClient

from pytest_types import DjangoAssertNumQueries
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser

from ...models import Customer


# Read
@pytest.mark.django_db
class TestWorkspaceCustomerRetrieve:
    """Test WorkspaceCustomerRetrieve."""

    @pytest.fixture
    def resource_url(
        self, paid_customer: Customer, workspace: Workspace
    ) -> str:
        """Return URL to resource."""
        return reverse("corporate:customers:read", args=(workspace.uuid,))

    def test_authenticated(
        self,
        user_client: APIClient,
        resource_url: str,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test as authenticated user."""
        with django_assert_num_queries(8):
            response = user_client.get(resource_url)
            assert response.status_code == 200, response.content


# RPC
class MockSession:
    """Checkout and billing portal mock session."""

    url = "https://www.example.com"


@pytest.fixture
def mock_stripe_checkout(
    settings: LazySettings,
    stripe_price_object: str,
) -> Iterable[mock.MagicMock]:
    """Mock stripe checkout session creation."""
    settings.STRIPE_PRICE_OBJECT = stripe_price_object
    with mock.patch("stripe.checkout.Session.create") as m:
        m.return_value = MockSession()
        yield m


@pytest.fixture
def mock_stripe_billing_portal() -> Iterable[mock.MagicMock]:
    """Mock stripe billing portal session creation."""
    with mock.patch("stripe.billing_portal.Session.create") as m:
        m.return_value = MockSession()
        yield m


@pytest.mark.django_db
class TestWorkspaceCheckoutSessionCreate:
    """Test creating a checkout session."""

    def test_invalid_uuid(
        self,
        mock_stripe_checkout: mock.MagicMock,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        faker: Faker,
    ) -> None:
        """Test passing in an invalid uuid."""
        resource_url = reverse(
            "corporate:customers:create-checkout-session",
            args=(str(faker.uuid4()),),
        )
        with django_assert_num_queries(2):
            response = rest_user_client.post(
                resource_url,
                data={"seats": 1337},
            )
            assert response.status_code == 400, response.data

    def test_posting_normal_data(
        self,
        mock_stripe_checkout: mock.MagicMock,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        unpaid_customer: Customer,
    ) -> None:
        """Test we can get a url when posting valid data."""
        resource_url = reverse(
            "corporate:customers:create-checkout-session",
            args=(str(unpaid_customer.workspace.uuid),),
        )
        with django_assert_num_queries(4):
            response = rest_user_client.post(
                resource_url,
                data={"seats": 1337},
            )
            assert response.status_code == 200, response.data
        assert response.data == {"url": "https://www.example.com"}

    def test_no_customer(
        self,
        mock_stripe_checkout: mock.MagicMock,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace_user: WorkspaceUser,
        workspace: Workspace,
    ) -> None:
        """Test it works even with no customer."""
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
        resource_url = reverse(
            "corporate:customers:create-checkout-session",
            args=(str(paid_customer.workspace.uuid),),
        )
        with django_assert_num_queries(2):
            response = rest_user_client.post(
                resource_url,
                data={"seats": 1337},
            )
            assert response.status_code == 400, response.data


@pytest.mark.django_db
class TestWorkspaceBillingPortalSessionCreate:
    """Test creating billing portal sessions."""

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
        with django_assert_num_queries(4):
            response = rest_user_client.post(resource_url)
            assert response.status_code == 403, response.data
        assert "no subscription is active" in response.data["detail"]

    def test_with_paying_customer(
        self,
        mock_stripe_billing_portal: mock.MagicMock,
        rest_user_client: APIClient,
        django_assert_num_queries: DjangoAssertNumQueries,
        paid_customer: Customer,
    ) -> None:
        """Test calling this with a paying customer."""
        resource_url = reverse(
            "corporate:customers:create-billing-portal-session",
            args=(str(paid_customer.workspace.uuid),),
        )
        with django_assert_num_queries(4):
            response = rest_user_client.post(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == {"url": "https://www.example.com"}
