"""Test stripe services in corporate app."""
import pytest
from rest_framework.exceptions import PermissionDenied

from corporate.models import Customer
from corporate.services.stripe import (
    create_billing_portal_session_for_workspace_uuid,
)
from workspace.models.workspace_user import WorkspaceUser


@pytest.mark.django_db
class TestCreateBillingPortalSessionForWorkspaceUuid:
    """Test create_billing_portal_session_for_workspace_uuid."""

    def test_missing_customer_id(
        self, workspace_user: WorkspaceUser, unpaid_customer: Customer
    ) -> None:
        """Test missing customer id will throw ValueError."""
        with pytest.raises(PermissionDenied) as error:
            create_billing_portal_session_for_workspace_uuid(
                workspace_uuid=unpaid_customer.workspace.uuid,
                who=workspace_user.user,
            )
        assert error.match("no subscription is active")
