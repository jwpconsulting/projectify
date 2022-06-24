"""Test corporate schema mutation."""
import pytest


@pytest.mark.django_db
class TestCustomerByWorkspace:
    """Test customerByWorkspace field."""

    query = """
query CustomerByWorkspace($workspaceUuid: UUID!) {
    customerByWorkspace(workspaceUuid: $workspaceUuid) {
        subscriptionStatus
        seats
        seatsRemaining
        uuid
        workspace {
            uuid
        }
    }
}
"""

    def test_query(
        self, graphql_query_user, workspace_user_customer, customer
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceUuid": str(customer.workspace.uuid),
            },
        )
        assert result == {
            "data": {
                "customerByWorkspace": {
                    "subscriptionStatus": "ACTIVE",
                    "seats": customer.seats,
                    "seatsRemaining": customer.seats_remaining,
                    "uuid": str(customer.uuid),
                    "workspace": {
                        "uuid": str(customer.workspace.uuid),
                    },
                },
            },
        }
