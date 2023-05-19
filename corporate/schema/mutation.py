"""Corporate schema mutations."""
import uuid

from django.conf import (
    settings,
)
from django.shortcuts import (
    get_object_or_404,
)

import strawberry

import stripe
from graphql import (
    GraphQLResolveInfo,
)
from workspace import models as workspace_models

from .. import (
    models,
)
from . import (
    types,
)


@strawberry.input
class CreateCheckoutSessionInput:
    """CreateCheckoutSession input."""

    workspace_uuid: uuid.UUID
    seats: int


@strawberry.input
class CreateBillingPortalSessionInput:
    """CreateBillingPortalSession mutation input."""

    uuid: uuid.UUID


@strawberry.type
class Mutation:
    """Mutation."""

    @strawberry.field
    def create_checkout_session(
        self, info: GraphQLResolveInfo, input: CreateCheckoutSessionInput
    ) -> types.CheckoutSession:
        """Create a Stripe checkout session."""
        qs = workspace_models.Workspace.objects.filter_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
        workspace = get_object_or_404(qs)
        try:
            customer = workspace.customer
            assert info.context.user.has_perm(
                "corporate.can_update_customer",
                customer,
            )
        except models.Customer.DoesNotExist:
            assert info.context.user.has_perm(
                "corporate.can_create_customer",
                workspace,
            )
            customer = models.Customer.objects.create(
                workspace=workspace, seats=input.seats
            )
        assert not customer.active
        session = stripe.checkout.Session.create(
            success_url=settings.FRONTEND_URL,
            cancel_url=settings.FRONTEND_URL,
            line_items=[
                {
                    "price": settings.STRIPE_PRICE_OBJECT,
                    "quantity": input.seats,
                },
            ],
            mode="subscription",
            subscription_data={"trial_period_days": 31},
            customer_email=info.context.user.email,
            metadata={"customer_uuid": customer.uuid},
        )
        return session

    @strawberry.field
    def create_billing_portal_session(
        self, info: GraphQLResolveInfo, input: CreateBillingPortalSessionInput
    ) -> types.BillingPortalSession:
        """Allow accessing the billing portal."""
        customer = models.Customer.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        assert info.context.user.has_perm(
            "corporate.can_update_customer",
            customer,
        )
        session = stripe.billing_portal.Session.create(
            customer=customer.stripe_customer_id,
            return_url=settings.FRONTEND_URL,
        )
        return session
