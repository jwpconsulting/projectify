# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Workspace URLs for dashboard."""

from django.urls import include, path

from projectify.workspace.views.dashboard import redirect_to_dashboard
from projectify.workspace.views.project import project_detail_view
from projectify.workspace.views.task import (
    task_create,
    task_create_sub_task_form,
    task_move,
)
from projectify.workspace.views.workspace import (
    workspace_list_view,
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
)
project_patterns = (
    # HTML
    path(
        "<uuid:project_uuid>",
        project_detail_view,
        name="detail",
    ),
)
section_patterns = (
    # Create task
    path("<uuid:section_uuid>/create-task", task_create, name="create-task"),
)
task_patterns = (
    # Form
    path("<uuid:task_uuid>/move", task_move, name="move"),
    path(
        "sub-task/<int:sub_tasks>",
        task_create_sub_task_form,
        name="create-task-sub-task",
    ),
)
urlpatterns = (
    path(
        "",
        redirect_to_dashboard,
        name="dashboard",
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
