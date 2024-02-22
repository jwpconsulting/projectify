# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""Test workspace model selectors."""
import pytest

from ...models.workspace_user import WorkspaceUser
from ...selectors.workspace import (
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ...services.workspace import workspace_delete

pytestmark = pytest.mark.django_db


def test_workspace_find_for_user(
    workspace_user: WorkspaceUser, unrelated_workspace_user: WorkspaceUser
) -> None:
    """Test workspace_find_for_user."""
    a = workspace_user
    b = unrelated_workspace_user
    assert workspace_find_for_user(who=a.user).count() == 1
    assert workspace_find_for_user(who=b.user).count() == 1
    workspace_delete(who=a.user, workspace=a.workspace)
    assert workspace_find_for_user(who=a.user).count() == 0
    assert workspace_find_for_user(who=b.user).count() == 1
    workspace_delete(who=b.user, workspace=b.workspace)
    assert workspace_find_for_user(who=a.user).count() == 0
    assert workspace_find_for_user(who=b.user).count() == 0


def test_workspace_find_by_workspace_uuid(
    workspace_user: WorkspaceUser, unrelated_workspace_user: WorkspaceUser
) -> None:
    """Test workspace_find_by_workspace_uuid."""
    a = workspace_user
    b = unrelated_workspace_user
    # A can find A's workspace
    assert workspace_find_by_workspace_uuid(
        who=a.user, workspace_uuid=a.workspace.uuid
    )
    # B can find B's workspace
    assert workspace_find_by_workspace_uuid(
        who=b.user, workspace_uuid=b.workspace.uuid
    )
    # A can't find B's workspace
    assert (
        workspace_find_by_workspace_uuid(
            who=a.user, workspace_uuid=b.workspace.uuid
        )
        is None
    )
    # B can't find A's workspace
    assert (
        workspace_find_by_workspace_uuid(
            who=b.user, workspace_uuid=a.workspace.uuid
        )
        is None
    )
