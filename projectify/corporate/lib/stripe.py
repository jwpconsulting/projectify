# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Stripe related helpers."""

from stripe import StripeClient

from projectify.lib.settings import get_settings


def stripe_client() -> StripeClient:
    """Return StripeClient from CorporateConfig."""
    settings = get_settings()
    secret_key = settings.STRIPE_SECRET_KEY
    if secret_key is None:
        raise ValueError("STRIPE_SECRET_KEY is not defined")
    return StripeClient(secret_key)
