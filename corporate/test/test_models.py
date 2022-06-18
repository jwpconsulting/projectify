"""Test corporate models."""
import pytest

from ..models import (
    Customer,
)


@pytest.mark.django_db
class TestCustomerManager:
    """Test Customer Manager."""

    def test_get_by_uuid(self, customer):
        """Test get Customer by UUID."""
        customer_by_manager = Customer.objects.get_by_uuid(customer.uuid)
        assert customer == customer_by_manager


@pytest.mark.django_db
class TestCustomer:
    """Test customer model."""

    def test_factory(self, customer):
        """Test factory."""
        assert customer.workspace

    def test_subscription_activation(self, unpaid_customer):
        """Test activating subscription."""
        assert not unpaid_customer.active
        unpaid_customer.activate_subscription()
        unpaid_customer.refresh_from_db()
        assert unpaid_customer.active

    def test_cancel_subscription(self, customer):
        """Test cancel_subscription."""
        assert customer.active
        customer.cancel_subscription()
        customer.refresh_from_db()
        assert not customer.active

    def test_assign_stripe_customer_id(self, customer):
        """Test assign_stripe_customer_id."""
        customer.assign_stripe_customer_id("Hello world")
        customer.refresh_from_db()
        assert customer.stripe_customer_id == "Hello world"

    def test_active(self, unpaid_customer):
        """Test active property."""
        assert not unpaid_customer.active
        unpaid_customer.activate_subscription()
        assert unpaid_customer.active
