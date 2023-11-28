"""Stripe related services."""
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import stripe
from rest_framework import serializers
from stripe.api_resources.billing_portal.session import (
    Session as BillingPortalSession,
)
from stripe.api_resources.checkout.session import Session

from projectify.utils import validate_perm
from user.models import User
from workspace.models.workspace import Workspace

from ..models import Customer


def checkout_session_create(
    *,
    who: User,
    workspace: Workspace,
    seats: int,
) -> Session:
    """Generate the URL for a checkout session."""
    try:
        customer = workspace.customer
        validate_perm(
            "corporate.can_update_customer",
            who,
            customer,
        )
    except Customer.DoesNotExist:
        validate_perm(
            "corporate.can_create_customer",
            who,
            workspace,
        )
        customer = Customer.objects.create(workspace=workspace, seats=seats)
    assert not customer.active
    if customer.active:
        raise serializers.ValidationError(
            _("This customer already has an active subscription")
        )
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


def create_billing_portal_session(
    *,
    who: User,
    customer: Customer,
) -> BillingPortalSession:
    """Allow accessing the billing portal."""
    validate_perm(
        "corporate.can_update_customer",
        who,
        customer,
    )
    session = stripe.billing_portal.Session.create(
        customer=customer.stripe_customer_id,
        return_url=settings.FRONTEND_URL,
    )
    return session
