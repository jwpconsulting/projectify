"""Corporate app urls."""
from django.urls import (
    include,
    path,
)

from corporate.views.custom_code import CustomCodeRedeem
from corporate.views.customer import (
    WorkspaceBillingPortalSessionCreate,
    WorkspaceCheckoutSessionCreate,
    WorkspaceCustomerRetrieve,
)
from corporate.views.stripe import stripe_webhook

app_name = "corporate"

customer_url_patterns = (
    # Read
    path(
        "<uuid:workspace_uuid>/customer",
        WorkspaceCustomerRetrieve.as_view(),
        name="read",
    ),
    # RPC
    path(
        "<uuid:workspace_uuid>/create-checkout-session",
        WorkspaceCheckoutSessionCreate.as_view(),
        name="create-checkout-session",
    ),
    path(
        "<uuid:workspace_uuid>/create-billing-portal-session",
        WorkspaceBillingPortalSessionCreate.as_view(),
        name="create-billing-portal-session",
    ),
)

custom_code_url_patterns = (
    # RPC
    path(
        "<uuid:workspace_uuid>/redeem-custom-code",
        CustomCodeRedeem.as_view(),
        name="redeem-custom-code",
    ),
)

urlpatterns = [
    # Customer
    path("workspace/", include((customer_url_patterns, "customers"))),
    # Custom code
    path("workspace/", include((custom_code_url_patterns, "custom-codes"))),
    # Stripe
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
]
