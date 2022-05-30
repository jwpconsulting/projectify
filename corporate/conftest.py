"""Corporate conftest."""
import pytest

from . import (
    factory,
)


@pytest.fixture
def customer():
    """Create customer."""
    return factory.CustomerFactory()


class MockStripeSessionResponse:
    """Mock StripeSessionResponse."""

    id = "cs_asdjkj123hj4h"


def mock_session(*args, **kwargs):
    """Fixture of MockStripeSessionResponse."""
    return MockStripeSessionResponse()
