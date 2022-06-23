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


class DottableDict(dict):
    """A dict that can be accessed by dot notation and by key."""

    def __init__(self, *args, **kwargs):
        """Initialize the dict."""
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class MockStripeCheckoutSession:
    """Dummy checkout session object."""

    customer = "unique_stripe_id"

    class metadata:
        """Metadata object."""

        customer_uuid = "asdj"


@pytest.fixture
def stripe_checkout_session_event_mock():
    """Mock the event sent by stripe."""
    mock_stripe_webhook_session = MockStripeCheckoutSession()
    event = DottableDict()
    event.type = "checkout.session.completed"
    event.data = {"object": mock_stripe_webhook_session}
    return event


@pytest.mark.django_db
class TestStripeWebhook:
    """Test incoming webhooks from Stripe."""

    def test_successful_checkout_webhook(
        self,
        unpaid_customer,
        stripe_checkout_session_event_mock,
        client,
    ):
        """Test the handling of a checkout session."""
        customer = unpaid_customer
        session = stripe_checkout_session_event_mock["data"]["object"]
        session.metadata.customer_uuid = customer.uuid

        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}

        with mock.patch("stripe.Webhook.construct_event") as construct_event:
            construct_event.return_value = stripe_checkout_session_event_mock
            response = client.post(reverse_lazy("stripe-webhook"), **header)
        assert response.status_code == 200
        customer.refresh_from_db()
        assert (
            customer.subscription_status
            == models.Customer.SubscriptionStatus.ACTIVE
        )
        assert customer.stripe_customer_id == "unique_stripe_id"
