"""Test Corporate mutations."""

from django.test import (
    Client,
)
from django.urls import (
    reverse_lazy,
)

import pytest

from corporate.models import (
    Customer,
)

from ..conftest import (
    mock_session,
)


@pytest.mark.django_db
class TestCreateCheckoutSession:
    """Test Create Stripe Checkout Session."""

    query = """
mutation createCheckoutSession ($workspaceUuid: UUID!, $seats: Int!) {
    createCheckoutSession(input: {workspaceUuid: $workspaceUuid, seats:$seats})
}
"""

    def test_query(
        self,
        graphql_query_user,
        customer,
        settings,
        monkeypatch,
        mock_session=mock_session,
    ):
        """Test query."""
        monkeypatch.setattr("stripe.checkout.Session.create", mock_session)
        settings.STRIPE_PRICE_OBJECT = "price_aklsdjw5er"
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceUuid": str(customer.workspace.uuid),
                "seats": customer.seats,
            },
        )

        assert result == {
            "data": {"createCheckoutSession": "cs_asdjkj123hj4h"}
        }


@pytest.mark.django_db
class TestStripeWebhook:
    """Test incoming webhooks from Stripe."""

    def test_successful_checkout_webhook(
        self,
        unpaid_customer,
        stripe_checkout_session_event_mock,
        monkeypatch,
    ):
        """Test the handling of a checkout session."""
        customer = unpaid_customer
        session = stripe_checkout_session_event_mock["data"]["object"]
        session.metadata.customer_uuid = customer.uuid

        def mock_event(*args, **kwargs):
            """Mock function."""
            return stripe_checkout_session_event_mock

        monkeypatch.setattr("stripe.Webhook.construct_event", mock_event)
        header = {"HTTP_STRIPE_SIGNATURE": "dummy_sig"}
        client = Client()
        response = client.post(reverse_lazy("stripe-webhook"), **header)
        customer.refresh_from_db()
        assert response.status_code == 200
        assert (
            customer.subscription_status == Customer.SubscriptionStatus.ACTIVE
        )
