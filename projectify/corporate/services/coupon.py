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
"""Coupon services."""
from typing import Optional

from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.corporate.types import CustomerSubscriptionStatus
from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace

from ..models.coupon import Coupon

# Took this as an inspiration
# https://github.com/tytso/pwgen/blob/1459a31e07fa208cddb2c4f3f72071503c37b8bc/pw_rand.c#L20
# But then figured sticking to lower case is easier to say when dictating
# coupon over telephone or other flaky communication channels and
# handwriting. Just in case.
COUPON_CHARS = "abcdefhijkmnpqrstuvwxy347"

# If we use the formula
#
# log_2(len(chars) ^ length)
# where len(chars) = 25
#
# suggested in get_random_string, we have
# length: 10, bit length =~ 32 bits
# length: 20, bit length =~ 64 bits
# Good enough? coupon creation isn't end-user facing anyway, so if
# in 1 out of 2^32 cases it fails, that's tolerable.


def coupon_create(
    *,
    who: User,
    seats: int,
    prefix: Optional[str] = None,
) -> Coupon:
    """Create a coupon for seats, for a user, with a given prefix."""
    suffix = get_random_string(10, COUPON_CHARS)
    code = f"{prefix}-{suffix}"
    validate_perm("corporate.create_coupon", who)
    return Coupon.objects.create(code=code, used=None, seats=seats)


@transaction.atomic
def coupon_redeem(
    *,
    who: User,
    code: str,
    workspace: Workspace,
) -> None:
    """Redeem a coupon for a workspace."""
    customer = workspace.customer
    validate_perm("corporate.can_update_customer", who, customer)
    try:
        # Make sure we lock the code to prevent race conditions
        coupon = (
            Coupon.objects.select_for_update()
            .filter(code=code, used__isnull=True)
            .get()
        )
    except Coupon.DoesNotExist:
        raise serializers.ValidationError(
            {"code": _("No coupon is available for this code")}
        )
    current_status = customer.subscription_status
    match current_status:
        case CustomerSubscriptionStatus.CUSTOM:
            raise serializers.ValidationError(
                _("A coupon has already been used for this workspace")
            )
        case CustomerSubscriptionStatus.ACTIVE:
            raise serializers.ValidationError(
                _("This workspace already has an active subscription")
            )
        case _:
            pass
    customer.subscription_status = CustomerSubscriptionStatus.CUSTOM
    customer.seats = coupon.seats
    customer.save()
    coupon.used = timezone.now()
    coupon.customer = customer
    coupon.save()
