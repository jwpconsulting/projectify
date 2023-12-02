"""Test user services."""
import pytest
from faker import Faker

from user.models import User
from user.services.user import (
    user_confirm_email,
    user_create,
    user_create_superuser,
    user_sign_up,
)


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
@pytest.mark.django_db
def test_user_confirm_email(user: User, inactive_user: User) -> None:
    """Test activating an active and inactive user."""
    assert user.is_active
    user_confirm_email(
        email=user.email,
        token=user.get_email_confirmation_token(),
    )
    user.refresh_from_db()
    assert user.is_active

    assert not inactive_user.is_active
    user_confirm_email(
        email=inactive_user.email,
        token=inactive_user.get_email_confirmation_token(),
    )
    inactive_user.refresh_from_db()
    assert inactive_user.is_active


# - user_log_in
# - user_log_out
# - user_request_password_reset
# - user_confirm_password_reset
