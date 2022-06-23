"""Test corporate models."""
from unittest import (
    mock,
)

import pytest

from .. import (
    models,
)


@pytest.mark.django_db
class TestCustomerManager:
    """Test Customer Manager."""

    def test_get_by_uuid(self, customer):
        """Test get Customer by UUID."""
        customer_by_manager = models.Customer.objects.get_by_uuid(
            customer.uuid
        )
        assert customer == customer_by_manager

    def test_get_by_workspace_uuid(self, customer):
        """Test get_by_workspace_uuid."""
        assert (
            models.Customer.objects.get_by_workspace_uuid(
                customer.workspace.uuid
            )
            == customer
        )

    def test_get_for_user_and_uuid(self, customer, workspace_user_customer):
        """Test get_for_user_and_uuid."""
        assert (
            models.Customer.objects.get_for_user_and_uuid(
                workspace_user_customer.user, customer.uuid
            )
            == customer
        )

    def test_get_by_stripe_customer_id(self, customer):
        """Test get_by_stripe_customer_id."""
        customer.stripe_customer_id = "hello_world"
        customer.save()
        assert (
            models.Customer.objects.get_by_stripe_customer_id(
                "hello_world",
            )
            == customer
        )


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

    def test_set_number_of_seats(self, customer):
        """Test set_number_of_seats."""
        original_seats = customer.seats
        customer.set_number_of_seats(original_seats + 1)
        customer.refresh_from_db()
        assert customer.seats == original_seats + 1

        customer.save = mock.MagicMock()
        customer.set_number_of_seats(customer.seats)
        assert not customer.save.called

    def test_active(self, unpaid_customer):
        """Test active property."""
        assert not unpaid_customer.active
        unpaid_customer.activate_subscription()
        assert unpaid_customer.active
