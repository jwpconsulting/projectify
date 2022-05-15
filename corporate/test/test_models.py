"""Test corporate models."""
import pytest


@pytest.mark.django_db
class TestCustomer:
    """Test customer model."""

    def test_factory(self, customer):
        """Test factory."""
        assert customer.workspace
