# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Corporate app urls."""

from django.urls import path

from projectify.corporate.views.stripe import stripe_webhook

app_name = "corporate"


urlpatterns = [
    # Stripe
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
]
