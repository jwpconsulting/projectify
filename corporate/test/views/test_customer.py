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
        return reverse("corporate:workspace-customer", args=(workspace.uuid,))

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
    faker: Faker,
) -> Iterable[mock.MagicMock]:
    """Mock stripe checkout session creation."""
    settings.STRIPE_PRICE_OBJECT = faker.bothify("price_???????#??")
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

    @pytest.fixture
    def resource_url(
        self,
        # Assuming unpaid customer
        unpaid_customer: Customer,
    ) -> str:
        """Return URL to this view."""
        return reverse(
            "corporate:customers:create-checkout-session",
            args=(str(unpaid_customer.workspace.uuid),),
        )

    def test_posting_normal_data(
        self,
        mock_stripe_checkout: mock.MagicMock,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test we can get a url when posting valid data."""
        with django_assert_num_queries(4):
            response = rest_user_client.post(
                resource_url,
                data={"seats": 1337},
            )
            assert response.status_code == 200, response.data
        assert response.data == {"url": "https://www.example.com"}


@pytest.mark.django_db
class TestWorkspaceBillingPortalSessionCreate:
    """Test creating billing portal sessions."""

    @pytest.fixture
    def resource_url(self, paid_customer: Customer) -> str:
        """Return URL to this view."""
        return reverse(
            "corporate:customers:create-billing-portal-session",
            args=(str(paid_customer.workspace.uuid),),
        )

    def test_with_paying_customer(
        self,
        mock_stripe_billing_portal: mock.MagicMock,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test calling this with a paying customer."""
        with django_assert_num_queries(4):
            response = rest_user_client.post(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == {"url": "https://www.example.com"}
