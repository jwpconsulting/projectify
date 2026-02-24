# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Workspace url patterns."""

from django.urls import include, path

from projectify.workspace.views.project import (
    ProjectArchive,
    ProjectCreate,
    ProjectReadUpdateDelete,
)
from projectify.workspace.views.section import (
    SectionCreate,
    SectionMove,
    SectionReadUpdateDelete,
)

from .views.team_member import TeamMemberReadUpdateDelete

app_name = "workspace"

workspace_patterns = ()

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

task_patterns = ()

label_patterns = ()

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
