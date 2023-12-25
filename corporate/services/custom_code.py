"""Custom code services."""
from typing import Optional

from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from corporate.types import CustomerSubscriptionStatus
from projectify.lib.auth import validate_perm
from user.models import User
from workspace.models.workspace import Workspace

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


@transaction.atomic
def custom_code_redeem(
    *,
    who: User,
    code: str,
    workspace: Workspace,
) -> None:
    """Redeem a custom code for a workspace."""
    customer = workspace.customer
    validate_perm("corporate.can_update_customer", who, customer)
    try:
        # Make sure we lock the code to prevent race conditions
        custom_code = (
            CustomCode.objects.select_for_update()
            .filter(code=code, used__isnull=True)
            .get()
        )
    except CustomCode.DoesNotExist:
        raise serializers.ValidationError(
            {"code": _("No custom code is available for this code")}
        )
    current_status = customer.subscription_status
    match current_status:
        case CustomerSubscriptionStatus.CUSTOM:
            raise serializers.ValidationError(
                _("A custom code has already been used for this workspace")
            )
        case CustomerSubscriptionStatus.ACTIVE:
            raise serializers.ValidationError(
                _("This workspace already has an active subscription")
            )
        case _:
            pass
    customer.subscription_status = CustomerSubscriptionStatus.CUSTOM
    customer.seats = custom_code.seats
    customer.save()
    custom_code.used = timezone.now()
    custom_code.customer = customer
    custom_code.save()
