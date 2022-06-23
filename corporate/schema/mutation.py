"""Corporate schema mutations."""
import uuid

from django.conf import (
    settings,
)

import strawberry

import stripe
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


@strawberry.type
class Mutation:
    """Mutation."""

    @strawberry.field
    def create_checkout_session(
        self, info, input: CreateCheckoutSessionInput
    ) -> types.CheckoutSession:
        """Create a Stripe checkout session."""
        workspace = workspace_models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
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
            metadata={"customer_uuid": customer.uuid},
        )
        return session
