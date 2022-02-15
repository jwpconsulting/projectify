"""User app schema mutation tests."""
import pytest


@pytest.mark.django_db
class TestSignupMutation:
    """Test Signup Mutation."""

    def test_user_is_created(self, graphql_query):
        """Assert that user is created."""
        query = """
mutation {
    signup(email: "hello@example.com", password: "password") {
        user {
            email
        }
    }
}
"""
        result = graphql_query(query)
        assert result == {
            "data": {
                "signup": {
                    "user": {
                        "email": "hello@example.com",
                    },
                }
            }
        }


@pytest.mark.django_db
class TestEmailConfirmationMutation:
    """Test Email Confirmation Mutation."""

    query = """
mutation($email: String!, $token: String!) {
    emailConfirmation(email: $email, token: $token) {
        user {
            email
        }
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
                    "user": {
                        "email": inactive_user.email,
                    },
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
  login(email: $email, password: $password) {
    user {
      email
    }
  }
}
"""

    def test_login_active_user(self, graphql_query, user):
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
                    "user": {
                        "email": user.email,
                    },
                }
            }
        }

    def test_login_wrong_password(self, graphql_query, user):
        """Test logging in with a wrong password."""
        result = graphql_query(
            self.query,
            variables={
                "email": user.email,
                "password": "wrongpassword",
            },
        )
        assert result == {"data": {"login": None}}

    def test_login_inactive_user(self, graphql_query, inactive_user):
        """Test logging in an inactive user."""
        result = graphql_query(
            self.query,
            variables={
                "email": inactive_user.email,
                "password": "password",
            },
        )
        assert result == {"data": {"login": None}}


@pytest.mark.django_db
class TestRequestPasswordResetMutation:
    """Test RequestPasswordResetMutation."""

    query = """
mutation RequestPasswordReset($email: String!) {
  requestPasswordReset(input: {email: $email}) {
    email
  }
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
  confirmPasswordReset(input: {
    email: $email, token: $token, newPassword: "password"
  }) {
    user {
      email
    }
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
                    "user": {
                        "email": user.email,
                    }
                }
            }
        }

    def test_invalid_token(self, graphql_query, user):
        """Test with an invalid token."""
        result = graphql_query(
            self.query,
            variables={
                "token": "beefcace",
                "email": user.email,
            },
        )
        assert result == {
            "data": {
                "confirmPasswordReset": {
                    "user": None,
                }
            }
        }
