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
"""Stripe related services."""
from uuid import UUID

from django.conf import settings
from django.utils.translation import gettext_lazy as _

import stripe
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from stripe.api_resources.billing_portal.session import (
    Session as BillingPortalSession,
)
from stripe.api_resources.checkout.session import Session

from corporate.selectors.customer import customer_find_by_workspace_uuid
from corporate.services.customer import (
    customer_create,
)
from projectify.lib.auth import validate_perm
from user.models import User
from workspace.selectors.workspace import workspace_find_by_workspace_uuid

from ..models import Customer


def stripe_checkout_session_create(
    *,
    customer: Customer,
    who: User,
    seats: int,
) -> Session:
    """Generate the URL for a checkout session."""
    if customer.stripe_customer_id is not None:
        raise serializers.ValidationError(
            _("This customer already activated a subscription before")
        )
    validate_perm("corporate.can_update_customer", who, customer)
    session = stripe.checkout.Session.create(
        success_url=settings.FRONTEND_URL,
        cancel_url=settings.FRONTEND_URL,
        line_items=[
            {
                "price": settings.STRIPE_PRICE_OBJECT,
                "quantity": seats,
            },
        ],
        mode="subscription",
        subscription_data={"trial_period_days": 31},
        customer_email=who.email,
        metadata={"customer_uuid": customer.uuid},
    )
    return session


def stripe_checkout_session_create_for_workspace_uuid(
    *, who: User, workspace_uuid: UUID, seats: int
) -> Session:
    """Create a checkout session given a workspace uuid."""
    # TODO maybe we can shortcut the below into a customer_find_by_workspace
    # and get the workspace first?
    customer = customer_find_by_workspace_uuid(
        workspace_uuid=workspace_uuid,
        who=who,
    )
    if customer is None:
        workspace = workspace_find_by_workspace_uuid(
            who=who, workspace_uuid=workspace_uuid
        )
        if workspace is None:
            raise serializers.ValidationError(
                {"workspace_uuid": _("No workspace found for this uuid")}
            )
        customer = customer_create(who=who, workspace=workspace, seats=seats)

    return stripe_checkout_session_create(
        customer=customer,
        who=who,
        seats=seats,
    )


# TODO change to create_billing_portal_session_for_workspace
# throw 404 in view instead
def create_billing_portal_session_for_workspace_uuid(
    *,
    who: User,
    workspace_uuid: UUID,
) -> BillingPortalSession:
    """Create a billing session for a user given a workspace uuid."""
    customer = customer_find_by_workspace_uuid(
        who=who,
        workspace_uuid=workspace_uuid,
    )
    if customer is None:
        raise serializers.ValidationError(
            {"workspace_uuid": _("No customer found for this workspace_uuid")}
        )
    validate_perm("corporate.can_update_customer", who, customer)
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
