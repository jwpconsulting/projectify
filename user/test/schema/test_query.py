"""Test user schema queries."""
import pytest


@pytest.mark.django_db
class TestQueryUser:
    """Test querying the user."""

    query = """
query {
    user {
        email
    }
}
"""

    def test_authenticated(self, user, graphql_query_user):
        """Test when authenticated."""
        result = graphql_query_user(self.query)
        assert result == {
            "data": {
                "user": {
                    "email": user.email,
                },
            },
        }

    def test_unauthenticated(self, graphql_query):
        """Test when unauthenticated."""
        result = graphql_query(self.query)
        assert result == {
            "data": {
                "user": None,
            },
        }
