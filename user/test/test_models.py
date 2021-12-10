"""Test user models."""
import pytest


@pytest.mark.django_db
class TestUser:
    """Test User class."""

    def test_factory(self, user):
        """Test user factory."""
        assert user.email

    def test_get_email_confirmation_token(self, user):
        """."""
        user.email = 'test@example'
        user.save()
        assert (
            user.get_email_confirmation_token() ==
            'd4aa423d5ee52b8d51ca9bbc7fd9d3acb7067855'
        )
