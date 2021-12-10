"""Test user models."""
import pytest


@pytest.mark.django_db
class TestUser:
    """Test User class."""

    def test_factory(self, user):
        """Test user factory."""
        assert user.email

    def test_get_email_confirmation_token(self, user):
        """Test retrieving the email confirmation token."""
        user.email = "test@example"
        assert (
            user.get_email_confirmation_token()
            == "d4aa423d5ee52b8d51ca9bbc7fd9d3acb7067855"
        )

    def test_check_email_confirmation_token(self, user):
        """Test checking the email confirmation token."""
        user.email = "test@example"
        assert (
            user.check_email_confirmation_token(
                "d4aa423d5ee52b8d51ca9bbc7fd9d3acb7067855"
            )
            is True
        )
        assert (
            user.check_email_confirmation_token(
                "e4aa423d5ee52b8d51ca9bbc7fd9d3acb7067855"
            )
            is False
        )
