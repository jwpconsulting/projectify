"""Test Corporate mutations."""
import pytest


class MockStripeSessionResponse:
    """Mock StripeSessionResponse."""

    id = "hello_world"


def mock_session(*args, **kwargs):
    """Fixture of MockStripeSessionResponse."""
    return MockStripeSessionResponse()


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
    ):
        """Test query."""
        monkeypatch.setattr("stripe.checkout.Session.create", mock_session)
        settings.STRIPE_PRICE_OBJECT = "price_aklsdjw5er"
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceUuid": str(customer.workspace.uuid),
                "seats": customer.seats,
            },
        )

        assert result == {"data": {"createCheckoutSession": "hello_world"}}
