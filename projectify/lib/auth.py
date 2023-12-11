"""Authorization and authentication related functions."""
# This is coupled to our own user model for now, otherwise we need to
# do lots of weird casting with AbstractBaseUser vs. AbstractUser
from typing import Any

from django.core.exceptions import PermissionDenied

from user.models import User


def validate_perm(
    perm: str,
    who: User,
    what: Any,
) -> bool:
    """Verify if who has perm to do what. Raise PermissionDenied otherwise."""
    if who.has_perm(perm, what):
        return True
    raise PermissionDenied(f"'{who}' can not '{perm}' for '{what}'")
