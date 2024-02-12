# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
