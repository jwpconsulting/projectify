"""Test customer model in corporate app."""
import pytest

from corporate.models import Customer
from corporate.services.customer import customer_check_active_for_workspace
from workspace.models.workspace import Workspace


@pytest.mark.django_db
def test_active(workspace: Workspace, unpaid_customer: Customer) -> None:
    """Test active property."""
    assert not customer_check_active_for_workspace(workspace=workspace)
    unpaid_customer.activate_subscription()
    assert customer_check_active_for_workspace(workspace=workspace)
