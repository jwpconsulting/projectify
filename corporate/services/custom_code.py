"""Custom code services."""
from typing import Optional

from django.utils.crypto import get_random_string

from projectify.lib.auth import validate_perm
from user.models import User

from ..models.custom_code import CustomCode

# Took this as an inspiration
# https://github.com/tytso/pwgen/blob/1459a31e07fa208cddb2c4f3f72071503c37b8bc/pw_rand.c#L20
# But then figured sticking to lower case is easier to say when dictating
# custom code over telephone or other flaky communication channels and
# handwriting. Just in case.
CUSTOM_CODE_CHARS = "abcdefhijkmnpqrstuvwxy347"

# If we use the formula
#
# log_2(len(chars) ^ length)
# where len(chars) = 25
#
# suggested in get_random_string, we have
# length: 10, bit length =~ 32 bits
# length: 20, bit length =~ 64 bits
# Good enough? custom code creation isn't end-user facing anyway, so if
# in 1 out of 2^32 cases it fails, that's tolerable.


def custom_code_create(
    *,
    who: User,
    seats: int,
    prefix: Optional[str] = None,
) -> CustomCode:
    """Create a custom code for seats, for a user, with a given prefix."""
    suffix = get_random_string(10, CUSTOM_CODE_CHARS)
    code = f"{prefix}-{suffix}"
    validate_perm("corporate.create_custom_code", who)
    return CustomCode.objects.create(code=code, used=None, seats=seats)
