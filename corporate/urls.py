"""Corporate app urls."""
from django.urls import (
    include,
    path,
)

from corporate.views.customer import (
    WorkspaceBillingPortalSessionCreate,
    WorkspaceCheckoutSessionCreate,
    WorkspaceCustomerRetrieve,
)
from corporate.views.stripe import stripe_webhook

app_name = "corporate"

customer_url_patterns = (
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

urlpatterns = [
    # Customer
    path("customer", include((customer_url_patterns, "customers"))),
    path(
        "workspace/<uuid:workspace_uuid>/customer",
        WorkspaceCustomerRetrieve.as_view(),
        name="workspace-customer",
    ),
    # Stripe
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
]
