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
"""Test project selectors."""
import pytest

from projectify.workspace.services.project import (
    project_archive,
)

from ...models.project import Project
from ...models.workspace_user import WorkspaceUser
from ...selectors.project import (
    project_find_by_project_uuid,
    project_find_by_workspace_uuid,
)

# So apparently this is also possible:
pytestmark = pytest.mark.django_db
# See https://docs.pytest.org/en/stable/example/markers.html#scoped-marking


def test_project_find_by_workspace_uuid(
    project: Project,
    workspace_user: WorkspaceUser,
    unrelated_workspace_user: WorkspaceUser,
) -> None:
    """Test project_find_by_workspace_uuid."""
    qs = project_find_by_workspace_uuid(
        who=workspace_user.user,
        workspace_uuid=workspace_user.workspace.uuid,
    )
    assert qs.get() == project

    # Unrelated user can not access
    qs = project_find_by_workspace_uuid(
        who=unrelated_workspace_user.user,
        workspace_uuid=workspace_user.workspace.uuid,
    )
    assert qs.count() == 0

    # Filter by ONLY archived, and we will get nothing
    qs = project_find_by_workspace_uuid(
        who=workspace_user.user,
        workspace_uuid=workspace_user.workspace.uuid,
        archived=True,
    )
    assert qs.count() == 0


def test_project_find_by_project_uuid(
    project: Project,
    workspace_user: WorkspaceUser,
    unrelated_workspace_user: WorkspaceUser,
    unrelated_project: Project,
) -> None:
    """Test finding project for a user by UUID."""
    # Normal case, user finds their project
    assert project_find_by_project_uuid(
        project_uuid=project.uuid,
        who=workspace_user.user,
    )
    # Unrelated user finds their board
    assert project_find_by_project_uuid(
        project_uuid=unrelated_project.uuid,
        who=unrelated_workspace_user.user,
    )
    # Unrelated workspace user does not have access
    assert (
        project_find_by_project_uuid(
            project_uuid=project.uuid,
            who=unrelated_workspace_user.user,
        )
        is None
    )
    # And our user can not see unrelated user's board
    assert (
        project_find_by_project_uuid(
            project_uuid=unrelated_project.uuid,
            who=workspace_user.user,
        )
        is None
    )

    # Archiving hides it unless passing extra flag
    project_archive(
        who=workspace_user.user,
        project=project,
        archived=True,
    )
    assert (
        project_find_by_project_uuid(
            project_uuid=project.uuid,
            who=workspace_user.user,
        )
        is None
    )
    # Passing archived will make it show up again
    assert project_find_by_project_uuid(
        project_uuid=project.uuid,
        who=workspace_user.user,
        archived=True,
    )
