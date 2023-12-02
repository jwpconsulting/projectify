"""User app schema mutation tests."""

import pytest


@pytest.mark.django_db
class TestUpdateProfileMutation:
    """Test UpdateProfileMutation."""

    query = """
mutation UpdateProfile {
    updateProfile(input: {fullName: "Foo Bar"}) {
        fullName
    }
}
"""

    def test_query(self, graphql_query_user):
        """Test query."""
        result = graphql_query_user(self.query)
        assert result == {
            "data": {
                "updateProfile": {
                    "fullName": "Foo Bar",
                },
            },
        }

    def test_query_unauthenticated(self, graphql_query):
        """Test query when unauthenticated."""
        result = graphql_query(self.query)
        assert result == {
            "data": {
                "updateProfile": None,
            },
        }
