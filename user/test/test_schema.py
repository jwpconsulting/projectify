"""User app schema tests."""

import pytest


@pytest.mark.django_db
class TestSignupMutation:
    """Test Signup Mutation."""

    def test_user_is_created(self, graphql_query, json_loads):
        query = """
mutation {
    signup(email: "hello@example.com", password: "password") {
        user {
            email
        }
    }
}
"""
        result = json_loads(graphql_query(query).content)
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
class TestLoginMutation:
    """Test LoginMutation."""

    query = """
mutation ($email: String!) {
  login(email: $email, password: "password") {
    user {
      email
    }
  }
}
"""

    def test_login_active_user(self, graphql_query, user, json_loads):
        """Test logging in an active user."""
        result = json_loads(
            graphql_query(self.query, variables={"email": user.email}).content
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

    def test_login_inactive_user(
        self, graphql_query, inactive_user, json_loads
    ):
        """Test logging in an inactive user."""
        result = json_loads(
            graphql_query(
                self.query, variables={"email": inactive_user.email}
            ).content
        )
        assert result == {"data": {"login": None}}
