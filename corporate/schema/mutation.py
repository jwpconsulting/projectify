"""Corporate schema mutations."""
import uuid

from django.conf import (
    settings,
)

import strawberry

import stripe
from workspace.models import (
    Workspace,
)

from ..models import (
    Customer,
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
    ) -> str:
        """Test creating a Stripe Checkout Session."""
        workspace = Workspace.objects.get(uuid=input.workspace_uuid)
        try:
            customer = workspace.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(
                workspace=workspace, seats=input.seats
            )
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
        return session.id
