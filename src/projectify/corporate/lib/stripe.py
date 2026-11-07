# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Stripe related helpers."""

from stripe import StripeClient

from projectify.lib.settings import get_settings


def stripe_client() -> StripeClient:
    """Return StripeClient from CorporateConfig."""
    config = get_settings().STRIPE_CONFIG
    if config is None:
        raise ValueError("You need to activate the Stripe integration.")
    return StripeClient(config.STRIPE_SECRET_KEY)
