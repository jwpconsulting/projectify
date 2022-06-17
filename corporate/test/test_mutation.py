"""Test Corporate mutations."""
import pytest

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
