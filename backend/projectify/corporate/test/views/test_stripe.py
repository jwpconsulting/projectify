# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Test stripe webhook."""

from unittest import (
    mock,
)

from django.urls import (
    reverse,
)

import pytest
from rest_framework.test import APIClient

from projectify.corporate.types import CustomerSubscriptionStatus
from projectify.settings.base import Base
from pytest_types import DjangoAssertNumQueries

from ...models import Customer

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def patch_stripe_settings(
    settings: Base, stripe_secret_key: str, stripe_endpoint_secret: str
) -> None:
    """Patch stripe settings."""
    settings.STRIPE_SECRET_KEY = stripe_secret_key
    settings.STRIPE_ENDPOINT_SECRET = stripe_endpoint_secret


class TestStripeWebhook:
    """Test incoming webhooks from Stripe."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to resource."""
        return reverse("corporate:stripe-webhook")

    @mock.patch("projectify.corporate.lib.stripe.StripeClient")
    def test_checkout_session_completed(
        self,
        stripe_client: mock.MagicMock,
        unpaid_customer: Customer,
        rest_client: APIClient,
        resource_url: str,
    ) -> None:
        """Test the handling of a checkout session."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}

        event = mock.MagicMock()
        event.type = "checkout.session.completed"
        event["data"]["object"].customer = "unique_stripe_id"
        # ["customer_uuid"]
        event["data"]["object"].metadata.get.return_value = str(
            unpaid_customer.uuid
        )
        line_item = mock.MagicMock()
        line_item.quantity = 13131313
        event["data"]["object"].list_line_items.return_value.data = [line_item]

        stripe_client.return_value.construct_event.return_value = event

        # TODO count queries
        response = rest_client.post(resource_url, **header)
        assert response.status_code == 200, response.data
        unpaid_customer.refresh_from_db()
        assert (
            unpaid_customer.subscription_status
            == CustomerSubscriptionStatus.ACTIVE
        )
        assert unpaid_customer.stripe_customer_id == "unique_stripe_id"
        assert unpaid_customer.seats == 13131313

    @mock.patch("projectify.corporate.lib.stripe.StripeClient")
    def test_customer_subscription_updated(
        self,
        stripe_client: mock.MagicMock,
        paid_customer: Customer,
        rest_client: APIClient,
        resource_url: str,
    ) -> None:
        """Test customer.subscription.updated."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}
        new_seats = paid_customer.seats + 1

        event = mock.MagicMock()
        event.type = "customer.subscription.updated"
        event["data"]["object"].customer = paid_customer.stripe_customer_id
        item_data = mock.MagicMock()
        item_data.quantity = new_seats
        stripe_client.return_value.subscription_items.list.return_value.data = [
            item_data
        ]

        stripe_client.return_value.construct_event.return_value = event

        # TODO count queries
        response = rest_client.post(resource_url, **header)
        assert response.status_code == 200, response.data
        paid_customer.refresh_from_db()
        assert paid_customer.seats == new_seats

    @mock.patch("projectify.corporate.lib.stripe.StripeClient")
    def test_customer_subscription_cancelled(
        self,
        stripe_client: mock.MagicMock,
        paid_customer: Customer,
        rest_client: APIClient,
        resource_url: str,
    ) -> None:
        """Test cancelling Subscription when payment fails."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}
        event = mock.MagicMock()
        event.type = "invoice.payment_failed"
        event["data"]["object"].customer = paid_customer.stripe_customer_id
        event["data"]["object"].next_payment_attempt = None
        stripe_client.return_value.construct_event.return_value = event

        # TODO count queries
        response = rest_client.post(resource_url, **header)
        assert response.status_code == 200, response.data
        paid_customer.refresh_from_db()
        assert (
            paid_customer.subscription_status
            == CustomerSubscriptionStatus.CANCELLED
        )

    @mock.patch("projectify.corporate.lib.stripe.StripeClient")
    def test_customer_subscription_deleted(
        self,
        stripe_client: mock.MagicMock,
        paid_customer: Customer,
        rest_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test cancelling Subscription when payment fails."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}
        event = mock.MagicMock()
        event.type = "customer.subscription.deleted"
        event["data"]["object"].customer = paid_customer.stripe_customer_id
        stripe_client.return_value.construct_event.return_value = event

        with django_assert_num_queries(2):
            response = rest_client.post(resource_url, **header)
        assert response.status_code == 200, response.data
        paid_customer.refresh_from_db()
        assert (
            paid_customer.subscription_status
            == CustomerSubscriptionStatus.CANCELLED
        )
