"""Test corporate models."""
import pytest

from ..models import (
    Customer,
)


@pytest.mark.django_db
class TestCustomer:
    """Test customer model."""

    def test_factory(self, customer):
        """Test factory."""
        assert customer.workspace

    def test_subscription_activation(self, unpaid_customer):
        """Test activating subscription."""
        customer = unpaid_customer
        customer.activate_subscription()
        customer.refresh_from_db()
        assert (
            customer.subscription_status == Customer.SubscriptionStatus.ACTIVE
        )


@pytest.mark.django_db
class TestCustomerManager:
    """Test Customer Manager."""

    def test_get_by_uuid(self, customer):
        """Test get Customer by UUID."""
        customer_by_manager = Customer.objects.get_by_uuid(customer.uuid)
        assert customer == customer_by_manager
