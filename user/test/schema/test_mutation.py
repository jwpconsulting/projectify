"""User app schema mutation tests."""
from typing import Any

import pytest

from user.models import User


@pytest.mark.django_db
class TestSignupMutation:
    """Test Signup Mutation."""

    def test_user_is_created(self, graphql_query):
        """Assert that user is created."""
        query = """
mutation {
    signup(input: {email: "hello@example.com", password: "password"}) {
        email
    }
}
"""
        result = graphql_query(query)
        assert result == {
            "data": {
                "signup": {
                    "email": "hello@example.com",
                },
            },
        }


@pytest.mark.django_db
class TestEmailConfirmationMutation:
    """Test Email Confirmation Mutation."""

    query = """
mutation($email: String!, $token: String!) {
    emailConfirmation(input: {email: $email, token: $token}) {
        email
    }
}
"""

    def test_user_is_activated(self, graphql_query, inactive_user):
        """Assert that user is activated."""
        assert inactive_user.is_active is False
        result = graphql_query(
            self.query,
            variables={
                "email": inactive_user.email,
                "token": inactive_user.get_email_confirmation_token(),
            },
        )
        assert result == {
            "data": {
                "emailConfirmation": {
                    "email": inactive_user.email,
                }
            }
        }
        inactive_user.refresh_from_db()
        assert inactive_user.is_active is True


@pytest.mark.django_db
class TestLoginMutation:
    """Test LoginMutation."""

    query = """
mutation ($email: String!, $password: String!) {
    login(input: {email: $email, password: $password}) {
        email
    }
}
"""

    def test_login_active_user(self, graphql_query: Any, user: User) -> None:
        """Test logging in an active user."""
        result = graphql_query(
            self.query,
            variables={
                "email": user.email,
                "password": "password",
            },
        )
        assert result == {
            "data": {
                "login": {
                    "email": user.email,
                }
            }
        }

    def test_login_wrong_password(
        self, graphql_query: Any, user: User
    ) -> None:
        """Test logging in with a wrong password."""
        result = graphql_query(
            self.query,
            variables={
                "email": user.email,
                "password": "wrongpassword",
            },
        )
        assert result["data"] == {"login": None}
        assert "could be found" in str(result["errors"])

    def test_login_inactive_user(
        self, graphql_query: Any, inactive_user: User
    ) -> None:
        """Test logging in an inactive user."""
        result = graphql_query(
            self.query,
            variables={
                "email": inactive_user.email,
                "password": "password",
            },
        )
        assert result["data"] == {"login": None}
        assert "could be found" in str(result["errors"])


@pytest.mark.django_db
class TestRequestPasswordResetMutation:
    """Test RequestPasswordResetMutation."""

    query = """
mutation RequestPasswordReset($email: String!) {
    requestPasswordReset(input: {email: $email})
}
"""

    def test_mutation(self, graphql_query, user, mailoutbox):
        """Test that an email is sent."""
        graphql_query(
            self.query,
            variables={
                "email": user.email,
            },
        )
        assert len(mailoutbox) == 1


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
