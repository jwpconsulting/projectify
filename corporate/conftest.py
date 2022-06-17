"""Corporate conftest."""
import pytest

from . import (
    factory,
    models,
)


@pytest.fixture
def customer():
    """Create customer."""
    return factory.CustomerFactory()


@pytest.fixture
def unpaid_customer():
    """Create unpaid customer."""
    customer = factory.CustomerFactory(
        subscription_status=models.Customer.SubscriptionStatus.UNPAID
    )
    return customer


class MockStripeSessionResponse:
    """Mock StripeSessionResponse."""

    id = "cs_asdjkj123hj4h"


def mock_session(*args, **kwargs):
    """Fixture of MockStripeSessionResponse."""
    return MockStripeSessionResponse()
