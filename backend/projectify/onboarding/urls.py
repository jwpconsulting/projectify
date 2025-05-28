# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Onboading urlpatterns."""

from django.urls import path

from projectify.onboarding.views import (
    about_you,
    new_label,
    new_project,
    new_task,
    new_workspace,
    welcome,
)

app_name = "onboarding"

urlpatterns = [
    path("welcome/", welcome, name="welcome"),
    path("about-you/", about_you, name="about_you"),
    path("new-workspace/", new_workspace, name="new_workspace"),
    path("new-project/<uuid:workspace_uuid>", new_project, name="new_project"),
    path("new-task/<uuid:project_uuid>", new_task, name="new_task"),
    path("new-label/<uuid:task_uuid>", new_label, name="new_label"),
]
