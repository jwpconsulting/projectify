# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Workspace url patterns."""
from django.urls import (
    include,
    path,
)

from projectify.workspace.views.label import LabelCreate, LabelUpdateDelete
from projectify.workspace.views.project import (
    ProjectArchive,
    ProjectArchivedList,
    ProjectCreate,
    ProjectReadUpdateDelete,
)
from projectify.workspace.views.section import (
    SectionCreate,
    SectionMove,
    SectionReadUpdateDelete,
)

from .views.task import (
    TaskCreate,
    TaskMoveAfterTask,
    TaskMoveToSection,
    TaskRetrieveUpdateDelete,
)
from .views.workspace import (
    InviteUserToWorkspace,
    UninviteUserFromWorkspace,
    UserWorkspaces,
    WorkspaceCreate,
    WorkspacePictureUploadView,
    WorkspaceReadUpdate,
)
from .views.team_member import (
    TeamMemberReadUpdateDelete,
)

app_name = "workspace"

workspace_patterns = (
    # Create
    path(
        "",
        WorkspaceCreate.as_view(),
        name="create",
    ),
    # Read + Update
    path(
        "<uuid:workspace_uuid>",
        WorkspaceReadUpdate.as_view(),
        name="read-update",
    ),
    # Read
    path(
        "user-workspaces/",
        UserWorkspaces.as_view(),
        name="user-workspaces",
    ),
    # Update
    # Delete
    # RPC
    path(
        "<uuid:workspace_uuid>/picture-upload",
        WorkspacePictureUploadView.as_view(),
        name="upload-picture",
    ),
    path(
        "<uuid:workspace_uuid>/invite-team-member",
        InviteUserToWorkspace.as_view(),
        name="invite-team-member",
    ),
    path(
        "<uuid:workspace_uuid>/uninvite-team-member",
        UninviteUserFromWorkspace.as_view(),
        name="uninvite-team-member",
    ),
    # Related
    # Archived projects
    path(
        "<uuid:workspace_uuid>/archived-projects/",
        ProjectArchivedList.as_view(),
        name="archived-projects",
    ),
)

team_member_patterns = (
    # Read + Update + Destroy
    path(
        "<uuid:team_member_uuid>",
        TeamMemberReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
)

project_patterns = (
    # Create
    path(
        "",
        ProjectCreate.as_view(),
        name="create",
    ),
    # Read + Update + Delete
    path(
        "<uuid:project_uuid>",
        ProjectReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
    # RPC
    path(
        "<uuid:project_uuid>/archive",
        ProjectArchive.as_view(),
        name="archive",
    ),
)

section_patterns = (
    # Create
    path(
        "",
        SectionCreate.as_view(),
        name="create",
    ),
    # Read + Update + Delete
    path(
        "<uuid:section_uuid>",
        SectionReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
    # RPC
    path(
        "<uuid:section_uuid>/move",
        SectionMove.as_view(),
        name="move",
    ),
)

task_patterns = (
    # Create
    path(
        "",
        TaskCreate.as_view(),
        name="create",
    ),
    # Read, Update, Delete
    path(
        "<uuid:task_uuid>",
        # TODO Rename all views to use standard CRUD terminology
        TaskRetrieveUpdateDelete.as_view(),
        name="read-update-delete",
    ),
    # RPC
    path(
        "<uuid:task_uuid>/move-to-section",
        TaskMoveToSection.as_view(),
        name="move-to-section",
    ),
    path(
        "<uuid:task_uuid>/move-after-task",
        TaskMoveAfterTask.as_view(),
        name="move-after-task",
    ),
)

label_patterns = (
    # Create
    path(
        "",
        LabelCreate.as_view(),
        name="create",
    ),
    # Read
    # Update
    path(
        "<uuid:label_uuid>",
        LabelUpdateDelete.as_view(),
        name="update-delete",
    ),
    # Delete
)

urlpatterns = (
    # Workspace
    path(
        "workspace/",
        include((workspace_patterns, "workspaces")),
    ),
    # TeamMember
    path(
        "team-member/",
        include((team_member_patterns, "team-members")),
    ),
    # Project
    path(
        "project/",
        include((project_patterns, "projects")),
    ),
    # Section
    path(
        "section/",
        include((section_patterns, "sections")),
    ),
    # Task
    path(
        "task/",
        include((task_patterns, "tasks")),
    ),
    # Label
    path("label/", include((label_patterns, "labels"))),
)
