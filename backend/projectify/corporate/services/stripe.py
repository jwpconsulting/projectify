# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
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
    logger.info("Customer %s updated to %d seats", customer, seats)


def customer_cancel_subscription(*, customer: Customer) -> None:
    """Cancel a customer's subscription."""
    customer.subscription_status = CustomerSubscriptionStatus.CANCELLED
    customer.save()
