# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""User model services in user app."""
import logging
from typing import Optional

from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.user.models.user import User

logger = logging.getLogger(__name__)


# No Create, since creating users is complicated


# Update
def user_update(
    *,
    who: User,
    user: User,
    preferred_name: Optional[str],
) -> User:
    """Update a user."""
    if not who == user:
        # TODO localize string
        raise PermissionDenied("User can only update own user")
    user.preferred_name = preferred_name
    user.save()
    return user


# RPC style
def user_change_password(
    *,
    user: User,
    old_password: str,
    new_password: str,
) -> None:
    """Change a user's password."""
    if not user.check_password(old_password):
        raise serializers.ValidationError(
            {"old_password": _("Incorrect password. Check again.")}
        )
    user.set_password(new_password)
    user.save()
