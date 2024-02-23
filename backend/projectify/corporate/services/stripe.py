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
"""
Corporate app services that are called from stripe webhook.

These functions all do not perform permission checks, so the caller has to
have validated permissions themselves.
"""
import logging

from ..models import Customer
from ..types import CustomerSubscriptionStatus

logger = logging.getLogger(__name__)


def customer_activate_subscription(
    *,
    customer: Customer,
    stripe_customer_id: str,
    seats: int,
) -> None:
    """Active a subscription for a customer."""
    customer.stripe_customer_id = stripe_customer_id
    customer.subscription_status = CustomerSubscriptionStatus.ACTIVE
    customer.seats = seats
    customer.save()


def customer_update_seats(*, customer: Customer, seats: int) -> None:
    """Update the number of seats for a customer."""
    # TODO Check why returning None is required
    if customer.seats == seats:
        logger.warning(
            "Customer %s set the same number of seats (%d) as before",
            str(customer.uuid),
            seats,
        )
        return None
    customer.seats = seats
    customer.save()


def customer_cancel_subscription(*, customer: Customer) -> None:
    """Cancel a customer's subscription."""
    customer.subscription_status = CustomerSubscriptionStatus.CANCELLED
    customer.save()
