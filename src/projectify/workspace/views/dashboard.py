# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""General dashboard views."""

from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.selectors.project import (
    project_find_by_workspace_uuid,
)
from projectify.workspace.selectors.team_member import (
    team_member_last_project_for_user,
    team_member_last_workspace_for_user,
)
from projectify.workspace.selectors.workspace import workspace_find_for_user


@platform_view
def redirect_to_dashboard(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Redirect to first available workspace or workspace list."""
    # TODO it would be fun if I could refactor this into a single call
    # that returns either a workspace or project
    # but still, if we're going to a workspace, we should remember what
    # project we looked at last
    maybe_last_visited_workspace = team_member_last_workspace_for_user(
        user=request.user
    )
    if maybe_last_visited_workspace:
        maybe_project = team_member_last_project_for_user(
            user=request.user, workspace=maybe_last_visited_workspace
        )
        if maybe_project:
            return redirect(maybe_project.get_absolute_url())
        return redirect(
            "dashboard:workspaces:detail",
            args=(maybe_last_visited_workspace.uuid,),
        )

    maybe_workspace = workspace_find_for_user(who=request.user).first()
    if not maybe_workspace:
        return redirect(reverse("onboarding:welcome"))

    maybe_project = project_find_by_workspace_uuid(
        workspace_uuid=maybe_workspace.uuid, who=request.user, archived=False
    ).first()
    if maybe_project:
        return redirect(maybe_project.get_absolute_url())

    return redirect(
        reverse(
            "onboarding:new_project",
            kwargs={"workspace_uuid": maybe_workspace.uuid},
        )
    )
