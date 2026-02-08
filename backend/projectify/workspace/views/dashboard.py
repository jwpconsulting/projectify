# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""General dashboard views."""

from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.workspace.selectors.project import (
    project_find_by_workspace_uuid,
)
from projectify.workspace.selectors.workspace import workspace_find_for_user


def redirect_to_dashboard(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Redirect to first available workspace or workspace list."""
    maybe_workspace = workspace_find_for_user(who=request.user).first()
    if not maybe_workspace:
        return redirect(reverse("onboarding:welcome"))

    maybe_project = project_find_by_workspace_uuid(
        workspace_uuid=maybe_workspace.uuid, who=request.user, archived=False
    ).first()
    if maybe_project:
        return redirect(
            reverse(
                "dashboard:projects:detail",
                kwargs={"project_uuid": maybe_project.uuid},
            )
        )

    return redirect(
        reverse(
            "onboarding:new_project",
            kwargs={"workspace_uuid": maybe_workspace.uuid},
        )
    )
