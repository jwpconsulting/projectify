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
"""Services for customer model."""

import logging
from typing import Any

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from stripe.billing_portal import (
    Session as BillingPortalSession,
)
from stripe.checkout import Session

from projectify.corporate.lib.stripe import stripe_client
from projectify.lib.auth import validate_perm
from projectify.lib.settings import get_settings
from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.selectors.quota import workspace_quota_for

from ..models import Customer

logger = logging.getLogger(__name__)


# Create
def customer_create(
    *, who: User, workspace: Workspace, seats: int
) -> Customer:
    """Create a customer."""
    validate_perm("corporate.can_create_customer", who, workspace)
    return Customer.objects.create(workspace=workspace, seats=seats)


# Update
# Delete


# RPC
def _billing_site_url(customer: Customer) -> str:
    """Return URL to customer.workspace's billing settings."""
    settings = get_settings()
    # XXX semi-hardcoded for now
    return (
        f"{settings.FRONTEND_URL}/dashboard/workspace/"
        f"{customer.workspace.uuid}/settings/billing"
    )


@transaction.atomic
def customer_create_stripe_checkout_session(
    *,
    customer: Customer,
    who: User,
    seats: int,
) -> Session:
    """Generate the URL for a checkout session."""
    workspace = customer.workspace
    validate_perm("corporate.can_update_customer", who, workspace)

    if customer.subscription_status == "ACTIVE":
        raise serializers.ValidationError(
            _("This customer already activated a subscription before")
        )

    # Ensure we can't ask for too few seats
    quota = workspace_quota_for(
        resource="TeamMemberAndInvite", workspace=workspace
    )
    if quota.current is None:
        logger.info("Customer for workspace %s has no seat quota")
    elif seats < quota.current:
        raise serializers.ValidationError(
            {
                "seats": _(
                    "Must request at least as many seats as current amount of team members and pending team member invites"
                )
            }
        )

    settings = get_settings()
    if settings.STRIPE_PRICE_OBJECT is None:
        raise ValueError("Expected STRIPE_PRICE_OBJECT")

    # XXX
    # Stripe types have invariance problems here
    line_items: list[Any] = [
        {
            "price": settings.STRIPE_PRICE_OBJECT,
            "quantity": seats,
        },
    ]
    client = stripe_client()
    match customer.stripe_customer_id:
        case str():
            session = client.checkout.sessions.create(
                params={
                    "success_url": _billing_site_url(customer),
                    # Same as above, perhaps we need a different one?
                    "cancel_url": _billing_site_url(customer),
                    "line_items": line_items,
                    "customer": customer.stripe_customer_id,
                    "mode": "subscription",
                    "metadata": {"customer_uuid": str(customer.uuid)},
                }
            )
        case None:
            session = client.checkout.sessions.create(
                params={
                    "success_url": _billing_site_url(customer),
                    # Same as above, perhaps we need a different one?
                    "cancel_url": _billing_site_url(customer),
                    "line_items": line_items,
                    "customer_email": who.email,
                    "mode": "subscription",
                    "metadata": {"customer_uuid": str(customer.uuid)},
                }
            )

    return session


def create_billing_portal_session_for_customer(
    *,
    who: User,
    customer: Customer,
) -> BillingPortalSession:
    """Create a billing session for a user given a workspace uuid."""
    validate_perm("corporate.can_update_customer", who, customer.workspace)
    customer_id = customer.stripe_customer_id
    if customer_id is None:
        raise serializers.ValidationError(
            _(
                "Can not create billing portal session because no "
                "subscription is active. If you believe this is an error, "
                "please contact support."
            )
        )
    client = stripe_client()
    return client.billing_portal.sessions.create(
        params={
            "customer": customer_id,
            "return_url": _billing_site_url(customer),
        }
    )
