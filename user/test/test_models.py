"""Test user models."""
import pytest

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


@pytest.mark.django_db
class TestUserInviteQuerySet:
    """Test UserInviteQuerySet."""

    def test_is_redeemed(
        self,
        user: User,
        redeemed_user_invite: UserInvite,
        user_invite: UserInvite,
    ) -> None:
        """Test is_redeemed."""
        assert UserInvite.objects.count() == 2
        assert UserInvite.objects.is_redeemed().count() == 1

    def test_by_email(self, redeemed_user_invite: UserInvite) -> None:
        """Test by_email."""
        user = redeemed_user_invite.user
        assert user is not None
        assert UserInvite.objects.by_email(user.email).count() == 1


@pytest.mark.django_db
class TestUserInvite:
    """Test UserInvite."""

    def test_factory(self, user_invite: UserInvite) -> None:
        """Test the factory."""
        assert user_invite.user is None

    def test_factory_redeemed(self, redeemed_user_invite: UserInvite) -> None:
        """Test the redeemed factory."""
        assert redeemed_user_invite.user is not None
