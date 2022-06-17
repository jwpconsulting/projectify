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
