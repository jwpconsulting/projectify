"""Corporate conftest."""
import pytest

from . import (
    factory,
)


@pytest.fixture
def customer():
    """Create customer."""
    return factory.CustomerFactory()
