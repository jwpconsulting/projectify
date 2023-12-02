"""User app schema mutation tests."""
from typing import Any

import pytest

from user.models import User


@pytest.mark.django_db
class TestConfirmPasswordResetMutation:
    """Test ConfirmPasswordResetMutation."""

    query = """
mutation ConfirmPasswordReset($token: String!, $email: String!) {
    confirmPasswordReset(
        input: {
            email: $email, token: $token, newPassword: "password"
    }) {
        email
    }
}
"""

    def test_valid_token(self, graphql_query, user):
        """Test with a valid token."""
        result = graphql_query(
            self.query,
            variables={
                "token": user.get_password_reset_token(),
                "email": user.email,
            },
        )
        assert result == {
            "data": {
                "confirmPasswordReset": {
                    "email": user.email,
                }
            }
        }

    def test_invalid_token(self, graphql_query: Any, user: User) -> None:
        """Test with an invalid token."""
        result = graphql_query(
            self.query,
            variables={
                "token": "beefcace",
                "email": user.email,
            },
        )
        assert result["data"] == {"confirmPasswordReset": None}
        assert "errors" in result


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
