"""Test corporate models."""
from unittest import (
    mock,
)

import pytest

from user import models as user_models
from workspace import models as workspace_models

from .. import (
    models,
)


@pytest.mark.django_db
class TestCustomerManager:
    """Test Customer Manager."""

    def test_get_by_uuid(self, customer: models.Customer) -> None:
        """Test get Customer by UUID."""
        customer_by_manager = models.Customer.objects.get_by_uuid(
            customer.uuid
        )
        assert customer == customer_by_manager

    def test_get_by_workspace_uuid(self, customer: models.Customer) -> None:
        """Test get_by_workspace_uuid."""
        assert (
            models.Customer.objects.get_by_workspace_uuid(
                customer.workspace.uuid
            )
            == customer
        )

    def test_filter_by_user(
        self,
        customer: models.Customer,
        workspace_user_customer: workspace_models.WorkspaceUser,
    ) -> None:
        """Test filter_by_user."""
        qs = models.Customer.objects.filter_by_user(
            workspace_user_customer.user
        )
        assert list(qs) == [customer]

    def test_get_for_user_and_uuid(
        self,
        customer: models.Customer,
        workspace_user_customer: workspace_models.WorkspaceUser,
    ) -> None:
        """Test get_for_user_and_uuid."""
        assert (
            models.Customer.objects.get_for_user_and_uuid(
                workspace_user_customer.user, customer.uuid
            )
            == customer
        )

    def test_get_by_stripe_customer_id(
        self, customer: models.Customer
    ) -> None:
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

    def test_factory(self, customer: models.Customer) -> None:
        """Test factory."""
        assert customer.workspace

    def test_subscription_activation(
        self, unpaid_customer: models.Customer
    ) -> None:
        """Test activating subscription."""
        assert not unpaid_customer.active
        unpaid_customer.activate_subscription()
        unpaid_customer.refresh_from_db()
        assert unpaid_customer.active

    def test_cancel_subscription(self, customer: models.Customer) -> None:
        """Test cancel_subscription."""
        assert customer.active
        customer.cancel_subscription()
        customer.refresh_from_db()
        assert not customer.active

    def test_assign_stripe_customer_id(
        self, customer: models.Customer
    ) -> None:
        """Test assign_stripe_customer_id."""
        customer.assign_stripe_customer_id("Hello world")
        customer.refresh_from_db()
        assert customer.stripe_customer_id == "Hello world"

    def test_set_number_of_seats(self, customer: models.Customer) -> None:
        """Test set_number_of_seats."""
        original_seats = customer.seats
        customer.set_number_of_seats(original_seats + 1)
        customer.refresh_from_db()
        assert customer.seats == original_seats + 1

        customer.save = mock.MagicMock()  # type: ignore
        customer.set_number_of_seats(customer.seats)
        assert not customer.save.called

    def test_active(self, unpaid_customer: models.Customer) -> None:
        """Test active property."""
        assert not unpaid_customer.active
        unpaid_customer.activate_subscription()
        assert unpaid_customer.active

    def test_seats_remaining(
        self, customer: models.Customer, user: user_models.User
    ) -> None:
        """Test seats remaining."""
        assert customer.seats_remaining == customer.seats
        customer.workspace.add_user(user)
        assert customer.seats_remaining == customer.seats - 1
        customer.workspace.invite_user(f"new+{user.email}")
        assert customer.seats_remaining == customer.seats - 2
