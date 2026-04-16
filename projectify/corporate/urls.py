# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Corporate app urls."""

import logging

from django.urls import path

from projectify.corporate.views.stripe import stripe_webhook
from projectify.lib.settings import get_settings
from projectify.lib.types import UrlPatterns

logger = logging.getLogger(__name__)

app_name = "corporate"


urlpatterns: UrlPatterns = []

settings = get_settings()

if settings.STRIPE_CONFIG is None:
    logger.info(
        "Stripe configuration not present. "
        "Did not install stripe-webhook view in Projectify URL patterns."
    )
else:
    urlpatterns = [
        *urlpatterns,
        # Stripe
        path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
    ]
