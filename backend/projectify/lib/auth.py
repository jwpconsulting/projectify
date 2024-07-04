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
import logging
from typing import Optional

from rest_framework.exceptions import PermissionDenied

from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace

logger = logging.getLogger(__name__)


def validate_perm(
    perm: str,
    who: User,
    where: Optional[Workspace] = None,
    raise_exception: bool = True,
) -> bool:
    """
    Verify if 'who' has permission 'perm' to do in Workspace 'where'.

    Raise PermissionDenied if no Permission and log warning.
    """
    if who.has_perm(perm, where):
        return True
    logger.warning(f"'{who}' did not have permission '{perm}' in '{where}'")
    if raise_exception:
        raise PermissionDenied(f"'{who}' can not '{perm}' in '{where}'")
    return False
