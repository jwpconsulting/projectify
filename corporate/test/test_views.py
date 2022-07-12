"""Test corporate app views."""
from unittest import (
    mock,
)

from django.urls import (
    reverse_lazy,
)

import pytest

from .. import (
    models,
)


@pytest.mark.django_db
class TestWorkspaceCustomerRetrieve:
    """Test WorkspaceCustomerRetrieve."""

    @pytest.fixture
    def resource_url(self, workspace):
        """Return URL to resource."""
        return reverse_lazy(
            "corporate:workspace-customer", args=(workspace.uuid,)
        )

    def test_authenticated(
        self,
        user_client,
        resource_url,
        customer,
        workspace_user_customer,
        django_assert_num_queries,
    ):
        """Test as authenticated user."""
        with django_assert_num_queries(8):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content


@pytest.mark.django_db
class TestStripeWebhook:
    """Test incoming webhooks from Stripe."""

    @pytest.fixture
    def resource_url(self):
        """Return URL to resource."""
        return reverse_lazy("corporate:stripe-webhook")

    def test_checkout_session_completed(
        self,
        unpaid_customer,
        client,
        resource_url,
    ):
        """Test the handling of a checkout session."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}

        event = mock.MagicMock()
        event.type = "checkout.session.completed"
        event["data"]["object"].customer = "unique_stripe_id"
        event["data"]["object"].metadata.customer_uuid = unpaid_customer.uuid

        with mock.patch("stripe.Webhook.construct_event") as construct_event:
            construct_event.return_value = event
            response = client.post(resource_url, **header)
        assert response.status_code == 200
        unpaid_customer.refresh_from_db()
        assert (
            unpaid_customer.subscription_status
            == models.CustomerSubscriptionStatus.ACTIVE
        )
        assert unpaid_customer.stripe_customer_id == "unique_stripe_id"

    def test_customer_subscription_updated(
        self, customer, client, resource_url
    ):
        """Test customer.subscription.updated."""
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}
        new_seats = customer.seats + 1

        event = mock.MagicMock()
        event.type = "customer.subscription.updated"
        event["data"]["object"].customer = customer.stripe_customer_id
        event["data"]["object"].quantity = new_seats

        with mock.patch("stripe.Webhook.construct_event") as construct_event:
            construct_event.return_value = event
            response = client.post(resource_url, **header)
        assert response.status_code == 200
        customer.refresh_from_db()
        assert customer.seats == new_seats
