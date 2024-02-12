# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Test user models."""
import pytest

from ..models import User, UserInvite


@pytest.mark.django_db
class TestUser:
    """Test User class."""

    def test_factory(self, user: User) -> None:
        """Test user factory."""
        assert user.email
        assert user.preferred_name is not None

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
