# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Workspace URLs for dashboard."""

from django.urls import include, path

from projectify.workspace.views.avatar_marble import avatar_marble_view
from projectify.workspace.views.dashboard import redirect_to_dashboard
from projectify.workspace.views.project import (
    project_archive_view,
    project_create_view,
    project_delete_view,
    project_detail_view,
    project_recover_view,
    project_update_view,
)
from projectify.workspace.views.section import (
    section_create_view,
    section_delete_view,
    section_update_view,
)
from projectify.workspace.views.task import (
    task_actions,
    task_create,
    task_create_sub_task_form,
    task_delete_view,
    task_detail,
    task_move,
    task_move_to_section,
    task_update_view,
)
from projectify.workspace.views.workspace import (
    workspace_list_view,
    workspace_settings_billing,
    workspace_settings_billing_edit,
    workspace_settings_edit_label,
    workspace_settings_general,
    workspace_settings_label,
    workspace_settings_new_label,
    workspace_settings_projects,
    workspace_settings_quota,
    workspace_settings_team_member_remove,
    workspace_settings_team_member_uninvite,
    workspace_settings_team_members,
    workspace_settings_team_members_invite,
    workspace_view,
)

app_name = "dashboard"
workspace_patterns = (
    # HTML
    path(
        "",
        workspace_list_view,
        name="list",
    ),
    path(
        "<uuid:workspace_uuid>",
        workspace_view,
        name="detail",
    ),
    # Project related views:
    path(
        "<uuid:workspace_uuid>/create-project",
        project_create_view,
        name="create-project",
    ),
    # Settings
    path(
        "<uuid:workspace_uuid>/settings",
        workspace_settings_general,
        name="settings",
    ),
    path(
        "<uuid:workspace_uuid>/projects",
        workspace_settings_projects,
        name="projects",
    ),
    path(
        "<uuid:workspace_uuid>/labels",
        workspace_settings_label,
        name="labels",
    ),
    path(
        "<uuid:workspace_uuid>/labels/create",
        workspace_settings_new_label,
        name="create-label",
    ),
    path(
        "<uuid:workspace_uuid>/labels/<uuid:label_uuid>",
        workspace_settings_edit_label,
        name="edit-label",
    ),
    path(
        "<uuid:workspace_uuid>/settings/team-members",
        workspace_settings_team_members,
        name="team-members",
    ),
    path(
        "<uuid:workspace_uuid>/settings/team-members/invite",
        workspace_settings_team_members_invite,
        name="team-members-invite",
    ),
    path(
        "<uuid:workspace_uuid>/team-member/<uuid:team_member_uuid>/remove",
        workspace_settings_team_member_remove,
        name="team-member-remove",
    ),
    path(
        "<uuid:workspace_uuid>/team-member/uninvite",
        workspace_settings_team_member_uninvite,
        name="team-member-uninvite",
    ),
    path(
        "<uuid:workspace_uuid>/settings/billing",
        workspace_settings_billing,
        name="billing",
    ),
    path(
        "<uuid:workspace_uuid>/settings/billing/edit",
        workspace_settings_billing_edit,
        name="billing-edit",
    ),
    path(
        "<uuid:workspace_uuid>/settings/quota",
        workspace_settings_quota,
        name="quota",
    ),
)
project_patterns = (
    path(
        "<uuid:project_uuid>",
        project_detail_view,
        name="detail",
    ),
    path(
        "<uuid:project_uuid>/update",
        project_update_view,
        name="update",
    ),
    path(
        "<uuid:project_uuid>/archive",
        project_archive_view,
        name="archive",
    ),
    path(
        "<uuid:project_uuid>/delete",
        project_delete_view,
        name="delete",
    ),
    path(
        "<uuid:project_uuid>/recover",
        project_recover_view,
        name="recover",
    ),
    # Create section
    path(
        "<uuid:project_uuid>/create-section",
        section_create_view,
        name="create-section",
    ),
)
section_patterns = (
    # Create task
    path("<uuid:section_uuid>/create-task", task_create, name="create-task"),
    # Update section
    path("<uuid:section_uuid>/update", section_update_view, name="update"),
    # Delete section
    path("<uuid:section_uuid>/delete", section_delete_view, name="delete"),
)
task_patterns = (
    path("<uuid:task_uuid>", task_detail, name="detail"),
    path("<uuid:task_uuid>/update", task_update_view, name="update"),
    # Move/delete actions menu
    path("<uuid:task_uuid>/actions", task_actions, name="actions"),
    path("<uuid:task_uuid>/delete", task_delete_view, name="delete"),
    # Form
    path("<uuid:task_uuid>/move", task_move, name="move"),
    path(
        "<uuid:task_uuid>/move-to-section",
        task_move_to_section,
        name="move-to-section",
    ),
    path(
        "sub-task/<int:sub_tasks>",
        task_create_sub_task_form,
        name="create-task-sub-task",
    ),
)
urlpatterns = (
    path("", redirect_to_dashboard, name="dashboard"),
    # Avatar
    path(
        "avatar/<uuid:team_member_uuid>.svg",
        avatar_marble_view,
        name="avatar-marble",
    ),
    # Workspace
    path(
        "workspace/",
        include((workspace_patterns, "workspaces")),
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
)
