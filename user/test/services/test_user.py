"""Test user services."""
import pytest

from user.services.user import user_create, user_create_superuser


@pytest.mark.django_db
def test_user_create() -> None:
    """Test creating a normal user."""
    u = user_create("hello@example")
    assert u.is_active is False


@pytest.mark.django_db
def test_user_create_superuser() -> None:
    """Test creating a superuser. A superuser should be active."""
    u = user_create_superuser("hello@example")
    assert u.is_active is True
