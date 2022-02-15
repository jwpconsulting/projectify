"""Test user models."""
import pytest

from ..models import (
    User,
)


@pytest.mark.django_db
class TestUserManager:
    """Test UserManager."""

    def test_create_user(self):
        """Test creating a normal user."""
        u = User.objects.create_user("hello@example")
        assert u.is_active is False

    def test_create_superuser(self):
        """Test creating a superuser. A superuser should be active."""
        u = User.objects.create_superuser("hello@example")
        assert u.is_active is True


@pytest.mark.django_db
class TestUser:
    """Test User class."""

    def test_factory(self, user):
        """Test user factory."""
        assert user.email
        assert user.full_name is not None

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
