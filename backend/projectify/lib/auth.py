# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Authorization and authentication related functions."""

# This is coupled to our own user model for now, otherwise we need to
# do lots of weird casting with AbstractBaseUser vs. AbstractUser
import logging
from typing import Union

from rest_framework.exceptions import PermissionDenied

from projectify.user.models import User
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace

logger = logging.getLogger(__name__)


# XXX support target, e.g., can user A delete user B?
def validate_perm(
    perm: str,
    who: User,
    target: Union[Workspace, TeamMember, None] = None,
    raise_exception: bool = True,
) -> bool:
    """
    Verify if 'who' has permission 'perm' for 'target'.

    Raise PermissionDenied if no Permission and log warning.
    """
    # XXX this is a bit of a workaround. I'm trying to make sure users
    # can't remove themselves from a workspace
    match target, perm:
        case (
            TeamMember(),
            "workspace.update_team_member_role"
            | "workspace.delete_team_member",
        ):
            pass
        case TeamMember(), _:
            raise ValueError(
                f"Target TeamMember with permission {perm} isn't supported"
            )
        case (
            _,
            "workspace.update_team_member_role"
            | "workspace.delete_team_member",
        ):
            raise ValueError(
                f"Target {type(target)} with permission {perm} isn't supported"
            )
        case _, _:
            pass
    if who.has_perm(perm, target):
        return True
    logger.warning(f"'{who}' doesn't have permission '{perm}' for '{target}'")
    if raise_exception:
        raise PermissionDenied(f"'{who}' can not '{perm}' for '{target}'")
    return False
