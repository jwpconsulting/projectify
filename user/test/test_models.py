"""Test user models."""
from unittest.mock import (
    MagicMock,
)

from django.dispatch import (
    receiver,
)

import pytest

from user.services.user_invite import user_invite_create

from .. import (
    factory,
    signal_defs,
)
from ..models import User, UserInvite


@pytest.mark.django_db
class TestUser:
    """Test User class."""

    def test_factory(self, user: User) -> None:
        """Test user factory."""
        assert user.email
        assert user.full_name is not None

    def test_get_email_confirmation_token(self, user: User) -> None:
        """Test retrieving the email confirmation token."""
        user.email = "test@example"
        assert (
            user.get_email_confirmation_token()
            == "d4aa423d5ee52b8d51ca9bbc7fd9d3acb7067855"
        )

    def test_check_email_confirmation_token(self, user: User) -> None:
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

    def test_redeem_invites(
        self,
        user: User,
        user_invite: UserInvite,
        redeemed_user_invite: UserInvite,
    ) -> None:
        """Test redeeming invites."""
        user_invite.email = user.email
        user_invite.save()
        assert not user_invite.redeemed
        user.redeem_invites()
        user_invite.refresh_from_db()
        assert user_invite.redeemed

    def test_redeem_multiple_invites(self, user: User) -> None:
        """Test what happens if invites exist. Nothing should happen."""
        factory.UserInviteFactory(email=user.email)
        factory.UserInviteFactory(email=user.email)
        user.redeem_invites()


@pytest.mark.django_db
class TestUserInviteQuerySet:
    """Test UserInviteQuerySet."""

    def test_is_redeemed(
        self, redeemed_user_invite: UserInvite, user_invite: UserInvite
    ) -> None:
        """Test is_redeemed."""
        assert UserInvite.objects.is_redeemed().count() == 1

    def test_by_email(
        self, redeemed_user_invite: UserInvite, user: UserInvite
    ) -> None:
        """Test by_email."""
        assert UserInvite.objects.by_email(user.email).count() == 1

    def test_invite_user(self) -> None:
        """Test inviting."""
        invite = user_invite_create(email="hello@example.com")
        assert invite

    def test_invite_twice(self) -> None:
        """Test inviting twice."""
        user_invite_create(email="hello@example.com")
        # Idempotent
        user_invite_create(email="hello@example.com")
        assert UserInvite.objects.count() == 1

    def test_invite_existing_user(self, user: User) -> None:
        """Ensure that inviting an existing user is impossible."""
        with pytest.raises(ValueError):
            user_invite_create(email=user.email)


@pytest.mark.django_db
class TestUserInvite:
    """Test UserInvite."""

    def test_factory(self, user_invite: UserInvite) -> None:
        """Test the factory."""
        assert user_invite.user is None

    def test_factory_redeemed(self, redeemed_user_invite: UserInvite) -> None:
        """Test the redeemed factory."""
        assert redeemed_user_invite.user is not None

    def test_redeem(self, user: User, user_invite: UserInvite) -> None:
        """Test redeeming."""
        mock = MagicMock()
        receiver(
            signal_defs.user_invitation_redeemed,
            sender=UserInvite,
        )(mock)
        user_invite.redeem(user)
        assert user_invite.user == user
        assert mock.called
