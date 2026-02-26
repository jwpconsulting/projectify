# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
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
class TestUserInvite:
    """Test UserInvite."""

    def test_factory(self, user_invite: UserInvite) -> None:
        """Test the factory."""
        assert user_invite.user is None

    def test_factory_redeemed(self, redeemed_user_invite: UserInvite) -> None:
        """Test the redeemed factory."""
        assert redeemed_user_invite.user is not None
