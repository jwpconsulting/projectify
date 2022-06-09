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


class DottableDict(dict):
    """A dict that can be accessed by dot notation and by key."""

    def __init__(self, *args, **kwargs):
        """Initialize the dict."""
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    def allowDotting(self, state=True):
        """Allow dot access."""
        if state:
            self.__dict__ = self
        else:
            self.__dict__ = dict()


class MockStripeCheckoutSession:
    """Dummy checkout session object."""

    customer = "unique_stripe_id"

    class metadata:
        """Metadata object."""

        customer_uuid = "asdj"


@pytest.fixture
def stripe_checkout_session_event_mock():
    """Mock the event sent by stripe."""
    mock_stripe_webhook_session = MockStripeCheckoutSession()
    event = DottableDict()
    event.allowDotting()
    event.type = "checkout.session.completed"
    event.data = {"object": mock_stripe_webhook_session}
    return event
