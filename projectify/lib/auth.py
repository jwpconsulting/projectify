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
"""Authorization and authentication related functions."""
# This is coupled to our own user model for now, otherwise we need to
# do lots of weird casting with AbstractBaseUser vs. AbstractUser
from typing import Any, Optional

from django.core.exceptions import PermissionDenied

from projectify.user.models import User


def validate_perm(
    perm: str,
    who: User,
    what: Optional[Any] = None,
) -> bool:
    """Verify if who has perm to do what. Raise PermissionDenied otherwise."""
    if who.has_perm(perm, what):
        return True
    raise PermissionDenied(f"'{who}' can not '{perm}' for '{what}'")
