import pytest


@pytest.mark.django_db
class TestUser:
    """Test User class."""

    def test_factory(self, user):
        """Test user factory."""
        assert user.email

