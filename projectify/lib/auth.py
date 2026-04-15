# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2024,2026 JWP Consulting GK
"""Authorization and authentication related functions."""

# This is coupled to our own user model for now, otherwise we need to
# do lots of weird casting with AbstractBaseUser vs. AbstractUser
import logging
from typing import Optional, Union
from uuid import UUID

from django.core.exceptions import PermissionDenied

from projectify.user.models import User
from projectify.workspace.models import TeamMember, Workspace

logger = logging.getLogger(__name__)

PermissionsCache = dict[tuple[str, UUID], bool]


# XXX support target, e.g., can user A delete user B?
def validate_perm(
    perm: str,
    who: User,
    target: Union[Workspace, TeamMember, None] = None,
    raise_exception: bool = True,
    cache: Optional[PermissionsCache] = None,
) -> bool:
    """
    Verify if 'who' has permission 'perm' for 'target'.

    Caches the result in the User object. This means that if a user instance
    contains stale caches permissions the user can or cannot do something
    that they're not supposed to.

    This should not be an issue since the "who" User is freshly created for each
    request by the authentication middleware.

    Log warning if no permission
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
    # Target is None when creating coupons
    if cache is not None and target is not None:
        cache_key = (perm, target.uuid)
        if cache_key in cache:
            result = cache[cache_key]
        else:
            result = who.has_perm(perm, target)
            cache[cache_key] = result
    else:
        result = who.has_perm(perm, target)
    if result is False:
        if raise_exception:
            raise PermissionDenied(f"'{who}' can not '{perm}' for '{target}'")
        logger.warning(
            f"'{who}' doesn't have permission '{perm}' for '{target}'"
        )
    return result
