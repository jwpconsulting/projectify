# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""User model selectors."""

from typing import Optional

from projectify.user.models import User


def user_find_by_email(*, email: str) -> Optional[User]:
    """Find a user by email."""
    try:
        return User.objects.get_by_natural_key(email)
    except User.DoesNotExist:
        return None
