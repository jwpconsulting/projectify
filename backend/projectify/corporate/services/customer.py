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
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import stripe
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from stripe.api_resources.billing_portal.session import (
    Session as BillingPortalSession,
)
from stripe.api_resources.checkout.session import Session

from projectify.corporate.types import (
    CustomerSubscriptionStatus,
    WorkspaceFeatures,
)
from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace

from ..models import Customer


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
def stripe_checkout_session_create(
    *,
    customer: Customer,
    who: User,
    seats: int,
) -> Session:
    """Generate the URL for a checkout session."""
    validate_perm("corporate.can_update_customer", who, customer.workspace)

    if customer.stripe_customer_id is not None:
        raise serializers.ValidationError(
            _("This customer already activated a subscription before")
        )

    # TODO
    # customer.seats = seats
    # customer.save()

    session = stripe.checkout.Session.create(
        # TODO Update url
        success_url=settings.FRONTEND_URL,
        # TODO Update url
        cancel_url=settings.FRONTEND_URL,
        line_items=[
            {"price": settings.STRIPE_PRICE_OBJECT, "quantity": seats},
        ],
        mode="subscription",
        subscription_data={"trial_period_days": 31},
        customer_email=who.email,
        metadata={"customer_uuid": customer.uuid},
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
        raise PermissionDenied(
            _(
                "Can not create billing portal session because no "
                "subscription is active. If you believe this is an error, "
                "please contact support."
            )
        )
    return stripe.billing_portal.Session.create(
        customer=customer.stripe_customer_id,
        return_url=settings.FRONTEND_URL,
    )


# TODO permissions needed?
# TODO check whether a workspace is in trial, then check further conditions
# TODO rename customer_check_workspace_features
def customer_check_active_for_workspace(
    *, workspace: Workspace
) -> WorkspaceFeatures:
    """Check if a customer is active for a given workspace."""
    try:
        customer = workspace.customer
    except Customer.DoesNotExist:
        raise ValueError(f"No customer found for workspace {workspace}")
    match customer.subscription_status:
        case CustomerSubscriptionStatus.ACTIVE:
            return "full"
        case CustomerSubscriptionStatus.CUSTOM:
            return "full"
        case CustomerSubscriptionStatus.UNPAID:
            return "trial"
        case CustomerSubscriptionStatus.CANCELLED:
            return "trial"
        case status:
            raise ValueError(f"Unknown status {status}")
