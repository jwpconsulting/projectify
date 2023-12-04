"""Test corporate models."""
from unittest import (
    mock,
)

import pytest
from faker import Faker

from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
)

from .. import (
    models,
)


@pytest.mark.django_db
class TestCustomerManager:
    """Test Customer Manager."""

    def test_get_by_uuid(self, unpaid_customer: models.Customer) -> None:
        """Test get Customer by UUID."""
        customer_by_manager = models.Customer.objects.get_by_uuid(
            unpaid_customer.uuid
        )
        assert unpaid_customer == customer_by_manager

    def test_get_by_workspace_uuid(
        self, unpaid_customer: models.Customer
    ) -> None:
        """Test get_by_workspace_uuid."""
        assert (
            models.Customer.objects.get_by_workspace_uuid(
                unpaid_customer.workspace.uuid
            )
            == unpaid_customer
        )

    def test_filter_by_user(
        self,
        unpaid_customer: models.Customer,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test filter_by_user."""
        qs = models.Customer.objects.filter_by_user(workspace_user.user)
        assert list(qs) == [unpaid_customer]

    def test_get_for_user_and_uuid(
        self,
        unpaid_customer: models.Customer,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test get_for_user_and_uuid."""
        assert (
            models.Customer.objects.get_for_user_and_uuid(
                workspace_user.user, unpaid_customer.uuid
            )
            == unpaid_customer
        )

    def test_get_by_stripe_customer_id(
        self, unpaid_customer: models.Customer
    ) -> None:
        """Test get_by_stripe_customer_id."""
        unpaid_customer.stripe_customer_id = "hello_world"
        unpaid_customer.save()
        assert (
            models.Customer.objects.get_by_stripe_customer_id(
                "hello_world",
            )
            == unpaid_customer
        )


@pytest.mark.django_db
class TestCustomer:
    """Test customer model."""

    def test_factory(self, unpaid_customer: models.Customer) -> None:
        """Test factory."""
        assert unpaid_customer.workspace

    def test_subscription_activation(
        self, unpaid_customer: models.Customer
    ) -> None:
        """Test activating subscription."""
        assert not unpaid_customer.active
        unpaid_customer.activate_subscription()
        unpaid_customer.refresh_from_db()
        assert unpaid_customer.active

    def test_cancel_subscription(self, paid_customer: models.Customer) -> None:
        """Test cancel_subscription."""
        assert paid_customer.active
        paid_customer.cancel_subscription()
        paid_customer.refresh_from_db()
        assert not paid_customer.active

    def test_assign_stripe_customer_id(
        self, unpaid_customer: models.Customer
    ) -> None:
        """Test assign_stripe_customer_id."""
        unpaid_customer.assign_stripe_customer_id("Hello world")
        unpaid_customer.refresh_from_db()
        assert unpaid_customer.stripe_customer_id == "Hello world"

    def test_set_number_of_seats(
        self, unpaid_customer: models.Customer
    ) -> None:
        """Test set_number_of_seats."""
        original_seats = unpaid_customer.seats
        unpaid_customer.set_number_of_seats(original_seats + 1)
        unpaid_customer.refresh_from_db()
        assert unpaid_customer.seats == original_seats + 1

        unpaid_customer.save = mock.MagicMock()  # type: ignore
        unpaid_customer.set_number_of_seats(unpaid_customer.seats)
        assert not unpaid_customer.save.called

    def test_active(self, unpaid_customer: models.Customer) -> None:
        """Test active property."""
        assert not unpaid_customer.active
        unpaid_customer.activate_subscription()
        assert unpaid_customer.active

    def test_seats_remaining(
        self,
        paid_customer: models.Customer,
        faker: Faker,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test seats remaining."""
        # user is already added, so there is already one seat used up
        assert paid_customer.seats_remaining == paid_customer.seats - 1
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=paid_customer.workspace,
            email_or_user=faker.email(),
        )
        assert paid_customer.seats_remaining == paid_customer.seats - 2
