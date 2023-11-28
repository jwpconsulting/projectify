"""Corporate schema mutations."""
import uuid

import strawberry
from graphql import (
    GraphQLResolveInfo,
)

from corporate.services.stripe import (
    create_billing_portal_session_for_workspace_uuid,
    stripe_checkout_session_create_for_workspace_uuid,
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

    workspace_uuid: uuid.UUID


@strawberry.type
class Mutation:
    """Mutation."""

    @strawberry.field
    def create_checkout_session(
        self, info: GraphQLResolveInfo, input: CreateCheckoutSessionInput
    ) -> types.CheckoutSession:
        """Create a Stripe checkout session."""
        return stripe_checkout_session_create_for_workspace_uuid(
            workspace_uuid=input.workspace_uuid,
            who=info.context.user,
            seats=input.seats,
        )  # type: ignore[return-value]

    @strawberry.field
    def create_billing_portal_session(
        self, info: GraphQLResolveInfo, input: CreateBillingPortalSessionInput
    ) -> types.BillingPortalSession:
        """Allow accessing the billing portal."""
        return create_billing_portal_session_for_workspace_uuid(
            who=info.context.user,
            workspace_uuid=input.workspace_uuid,
        )  # type: ignore[return-value]
