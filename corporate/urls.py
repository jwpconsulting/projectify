"""Corporate app urls."""
from django.urls import (
    path,
)

from .views import (
    stripe_webhook,
)


urlpatterns = [
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
]
