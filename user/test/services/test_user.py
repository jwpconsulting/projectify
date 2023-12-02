"""Test user services."""
import pytest
from faker import Faker

from user.models import User
from user.services.user import user_create, user_create_superuser, user_sign_up


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


@pytest.mark.django_db
def test_user_sign_up(faker: Faker) -> None:
    """Test signing up a new user."""
    assert User.objects.count() == 0
    user_sign_up(email=faker.email(), password=faker.password())
    assert User.objects.count() == 1


# TODO
# - user_confirm_email
# - user_log_in
# - user_log_out
# - user_request_password_reset
# - user_confirm_password_reset
