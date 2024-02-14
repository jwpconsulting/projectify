# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Internal services, not user facing."""
from datetime import datetime
from typing import Optional

from django.contrib.auth.hashers import make_password

from projectify.user.models.user import User
from projectify.user.services.user_invite import user_invite_redeem_many


def _user_create(
    email: str,
    password: Optional[str],
    is_staff: bool,
    is_superuser: bool,
    is_active: bool,
    tos_agreed: Optional[datetime] = None,
    privacy_policy_agreed: Optional[datetime] = None,
) -> User:
    """Create and save a user with the given email, and password."""
    email = User.objects.normalize_email(email)
    user = User(
        email=email,
        is_staff=is_staff,
        is_superuser=is_superuser,
        is_active=is_active,
        tos_agreed=tos_agreed,
        privacy_policy_agreed=privacy_policy_agreed,
    )
    user.password = make_password(password)
    # XXX self._db needed? user.save(using=self._db)
    user.save()
    user_invite_redeem_many(user=user)
    return user


def user_create(
    *,
    email: str,
    password: Optional[str] = None,
    tos_agreed: Optional[datetime] = None,
    privacy_policy_agreed: Optional[datetime] = None,
) -> User:
    """Create a normal user."""
    return _user_create(
        email,
        password,
        is_staff=False,
        is_superuser=False,
        is_active=False,
        tos_agreed=tos_agreed,
        privacy_policy_agreed=privacy_policy_agreed,
    )


def user_create_superuser(
    *,
    email: str,
    password: Optional[str] = None,
) -> "User":
    """Create a superuser."""
    return _user_create(
        email,
        password,
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )
