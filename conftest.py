import pytest

from user.factory import UserFactory

@pytest.fixture
def user():
    """Return a db user."""
    return UserFactory.create()
