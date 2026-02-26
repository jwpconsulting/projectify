# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test customer services in corporate app."""

from collections.abc import Iterable
from unittest import mock

import pytest
from rest_framework import serializers

from projectify.corporate.models import Customer
from projectify.corporate.services.customer import (
    customer_create_stripe_checkout_session,
)
from projectify.settings.base import Base
from projectify.workspace.models import TeamMember

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def patch_stripe_settings(
    settings: Base,
    stripe_price_object: str,
    stripe_secret_key: str,
    stripe_endpoint_secret: str,
) -> None:
    """Patch stripe settings."""
    settings.STRIPE_SECRET_KEY = stripe_secret_key
    settings.STRIPE_ENDPOINT_SECRET = stripe_endpoint_secret
    settings.STRIPE_PRICE_OBJECT = stripe_price_object


# TODO DRY this, duplicated from corporate/test/views/test_customer.py
class MockSession:
    """Checkout and billing portal mock session."""

    url = "https://www.example.com"


class TestCustomerCreateStripeCheckoutSession:
    """Test customer_create_stripe_checkout_session."""

    @pytest.fixture(autouse=True)
    def mock_stripe_checkout(
        self,
    ) -> Iterable[mock.MagicMock]:
        """Mock stripe checkout session creation."""
        with mock.patch(
            "stripe.checkout._session_service.SessionService.create"
        ) as m:
            m.return_value = MockSession()
            yield m

    def test_too_few_seats(
        self, unpaid_customer: Customer, team_member: TeamMember
    ) -> None:
        """Assert that a minimum amount of seats is ensured."""
        seats = unpaid_customer.workspace.users.count()
        with pytest.raises(serializers.ValidationError):
            customer_create_stripe_checkout_session(
                who=team_member.user,
                customer=unpaid_customer,
                seats=seats - 1,
            )
        customer_create_stripe_checkout_session(
            who=team_member.user,
            customer=unpaid_customer,
            seats=seats,
        )
