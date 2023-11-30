"""Test user invite services."""
import pytest

from user.models import User, UserInvite
from user.services.user_invite import user_invite_create


@pytest.mark.django_db
def test_invite_user() -> None:
    """Test inviting."""
    invite = user_invite_create(email="hello@example.com")
    assert invite


@pytest.mark.django_db
def test_invite_twice() -> None:
    """Test inviting twice."""
    user_invite_create(email="hello@example.com")
    # Idempotent
    user_invite_create(email="hello@example.com")
    assert UserInvite.objects.count() == 1


@pytest.mark.django_db
def test_invite_existing_user(user: User) -> None:
    """Ensure that inviting an existing user is impossible."""
    with pytest.raises(ValueError):
        # TODO in the future, there will be no ValueError and we will
        # get None instead.
        user_invite_create(email=user.email)
