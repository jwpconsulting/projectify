"""Test user models."""
from unittest.mock import (
    MagicMock,
)

from django.dispatch import (
    receiver,
)

import pytest

from .. import (
    models,
    signals,
)


@pytest.mark.django_db
class TestUserManager:
    """Test UserManager."""

    def test_create_user(self):
        """Test creating a normal user."""
        u = models.User.objects.create_user("hello@example")
        assert u.is_active is False

    def test_create_superuser(self):
        """Test creating a superuser. A superuser should be active."""
        u = models.User.objects.create_superuser("hello@example")
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

    def test_redeem_invites(self, user, user_invite, redeemed_user_invite):
        """Test redeeming invites."""
        user_invite.email = user.email
        user_invite.save()
        assert not user_invite.redeemed
        user.redeem_invites()
        user_invite.refresh_from_db()
        assert user_invite.redeemed


@pytest.mark.django_db
class TestUserInviteQuerySet:
    """Test UserInviteQuerySet."""

    def test_is_redeemed(self, redeemed_user_invite, user_invite):
        """Test is_redeemed."""
        assert models.UserInvite.objects.is_redeemed().count() == 1

    def test_by_email(self, redeemed_user_invite, user):
        """Test by_email."""
        assert models.UserInvite.objects.by_email(user.email).count() == 1

    def test_invite_user(self):
        """Test inviting."""
        invite = models.UserInvite.objects.invite_user("hello@example.com")
        assert invite

    def test_invite_twice(self):
        """Test inviting twice."""
        models.UserInvite.objects.invite_user("hello@example.com")
        # Works
        models.UserInvite.objects.invite_user("hello@example.com")

    def test_invite_existing_user(self, user):
        """Ensure that inviting an existing user is impossible."""
        with pytest.raises(ValueError):
            models.UserInvite.objects.invite_user(user.email)


@pytest.mark.django_db
class TestUserInvite:
    """Test UserInvite."""

    def test_factory(self, user_invite):
        """Test the factory."""
        assert user_invite.user is None

    def test_factory_redeemed(self, redeemed_user_invite):
        """Test the redeemed factory."""
        assert redeemed_user_invite.user is not None

    def test_redeem(self, user, user_invite):
        """Test redeeming."""
        mock = MagicMock()
        receiver(
            signals.user_invitation_redeemed,
            sender=models.UserInvite,
        )(mock)
        user_invite.redeem(user)
        assert user_invite.user == user
        assert mock.called
