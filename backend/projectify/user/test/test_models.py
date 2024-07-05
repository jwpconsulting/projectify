# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021-2024 JWP Consulting GK
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

from django.core.exceptions import ValidationError

import pytest

from ..models import User, UserInvite


@pytest.mark.django_db
class TestUser:
    """Test User class."""

    def test_factory(self, user: User) -> None:
        """Test user factory."""
        assert user.email
        assert user.preferred_name is not None

    def test_preferred_name_validation(self, user: User) -> None:
        """Test url like names can not be inserted."""
        # Rejected
        user.preferred_name = "www.google.com"
        with pytest.raises(ValidationError):
            user.full_clean()

        user.preferred_name = "www.google.com."
        with pytest.raises(ValidationError):
            user.full_clean()

        user.preferred_name = "http://localhost"
        with pytest.raises(ValidationError):
            user.full_clean()

        # Allowed
        user.preferred_name = "John McHurDur Jr."
        user.full_clean()

        user.preferred_name = "http: //localhost"
        user.full_clean()

        user.preferred_name = "Department of: silly walks"
        user.full_clean()

        user.preferred_name = "www. google"
        user.full_clean()

        user.preferred_name = "Foob. Ar"
        user.full_clean()

        user.preferred_name = ""
        user.full_clean()
        user.save()

        user.preferred_name = None
        user.full_clean()
        user.save()


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
