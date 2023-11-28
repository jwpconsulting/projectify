"""Test Corporate mutations."""
from typing import Any
from unittest import (
    mock,
)

import pytest

from conftest import QueryMethod
from corporate.models import Customer
from workspace.models.workspace_user import WorkspaceUser


@pytest.mark.django_db
class TestCreateCheckoutSession:
    """Test Create Stripe Checkout Session."""

    query = """
mutation createCheckoutSession ($workspaceUuid: UUID!, $seats: Int!) {
    createCheckoutSession(
        input: {workspaceUuid: $workspaceUuid, seats: $seats}
    ) {
        stripeId
    }
}
"""

    def test_query_unpaid_customer(
        self,
        graphql_query_user: QueryMethod,
        unpaid_customer: Customer,
        settings: Any,
        workspace_user_unpaid_customer: WorkspaceUser,
    ) -> None:
        """Test query with unpaid customer."""
        settings.STRIPE_PRICE_OBJECT = "price_aklsdjw5er"
        with mock.patch("stripe.checkout.Session.create") as create:
            create.return_value.id = "hello_world"
            result = graphql_query_user(
                self.query,
                variables={
                    "workspaceUuid": str(unpaid_customer.workspace.uuid),
                    "seats": unpaid_customer.seats,
                },
            )
        assert result == {
            "data": {
                "createCheckoutSession": {
                    "stripeId": "hello_world",
                },
            },
        }

    def test_query_no_customer(
        self,
        graphql_query_user,
        unpaid_customer,
        settings,
        workspace_user_unpaid_customer,
    ):
        """Test query with missing customer."""
        workspace = unpaid_customer.workspace
        unpaid_customer.delete()
        settings.STRIPE_PRICE_OBJECT = "price_aklsdjw5er"
        with mock.patch("stripe.checkout.Session.create") as create:
            create.return_value.id = "hello_world"
            result = graphql_query_user(
                self.query,
                variables={
                    "workspaceUuid": str(workspace.uuid),
                    "seats": 1,
                },
            )
        assert result == {
            "data": {
                "createCheckoutSession": {
                    "stripeId": "hello_world",
                },
            },
        }

    def test_query_paid_customer(
        self,
        graphql_query_user,
        customer,
        settings,
        workspace_user_customer,
    ):
        """Test query with paid customer."""
        workspace = customer.workspace
        settings.STRIPE_PRICE_OBJECT = "price_aklsdjw5er"
        with mock.patch("stripe.checkout.Session.create") as create:
            create.return_value.id = "hello_world"
            result = graphql_query_user(
                self.query,
                variables={
                    "workspaceUuid": str(workspace.uuid),
                    "seats": 1,
                },
            )
        assert "errors" in result


@pytest.mark.django_db
class TestCreateBillingPortalSession:
    """Test createBillingPortalSession mutation."""

    query = """
mutation CreateBillingPortalSession($workspaceUuid: UUID!) {
    createBillingPortalSession(input: {workspaceUuid: $workspaceUuid}) {
        url
    }
}
"""

    def test_query_paid_customer(
        self,
        graphql_query_user: QueryMethod,
        customer: Customer,
        settings: Any,
        workspace_user_customer: WorkspaceUser,
    ) -> None:
        """Test query with paid customer."""

        class Session:
            """Billing portal mock session."""

            url = "https://www.example.com/"

        with mock.patch("stripe.billing_portal.Session.create") as create:
            create.return_value = Session()
            result = graphql_query_user(
                self.query,
                variables={
                    "workspaceUuid": str(customer.workspace.uuid),
                },
            )
        assert result == {
            "data": {
                "createBillingPortalSession": {
                    "url": "https://www.example.com/",
                },
            },
        }
