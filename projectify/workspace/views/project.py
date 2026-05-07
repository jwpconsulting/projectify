# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2026 JWP Consulting GK
"""Project views."""

import logging
from typing import Any, Optional, TypeVar, Union
from uuid import UUID

from django import forms
from django.core.exceptions import BadRequest
from django.db.models import Model, QuerySet
from django.forms import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from projectify.lib.forms import RichTextEditor, populate_form_with_errors
from projectify.lib.htmx import HttpResponseClientRefresh
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.utils import strip_first_paragraph
from projectify.lib.views import platform_view
from projectify.workspace.const import TASK_EDITOR_MIN_HEIGHT_CLASS

from ..models import Project, Task, TeamMember, Workspace
from ..selectors.project import (
    project_detail_query_set,
    project_find_by_project_uuid,
)
from ..selectors.quota import workspace_get_all_quotas
from ..selectors.team_member import team_member_find_for_workspace
from ..selectors.workspace import (
    workspace_build_detail_query_set,
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ..services.project import (
    project_archive,
    project_create,
    project_delete,
    project_update,
)
from ..services.task import task_create, task_mark_done
from ..services.team_member import (
    team_member_minimize_team_member_filter,
    team_member_visit_project,
)

logger = logging.getLogger(__name__)

Q = TypeVar("Q", bound=Model)


def get_project_view_context(
    request: AuthenticatedHttpRequest, workspace: Workspace
) -> dict[str, object]:
    """Get shared context for project views."""
    if not hasattr(workspace, "current_team_member_qs"):
        current_team_member = team_member_find_for_workspace(
            user=request.user, workspace=workspace
        )
        logger.warning("No current_team_member_qs in workspace")
    else:
        current_team_member_qs: Union[list[TeamMember], TeamMember, Any] = (
            getattr(workspace, "current_team_member_qs")
        )
        match current_team_member_qs:
            case TeamMember() as current_team_member:
                pass
            case [current_team_member]:
                pass
            case any:
                raise RuntimeError(f"Don't know what to do with {type(any)}")
    return {
        "workspace": workspace,
        "workspaces": workspace_find_for_user(who=request.user),
        "projects": workspace.project_set.all(),
        "current_team_member_qs": current_team_member,
    }


class TaskQuickAddForm(forms.Form):
    """Form for adding tasks with just a title."""

    title = forms.CharField(
        label=_("Task title"),
        widget=forms.TextInput(attrs={"placeholder": _("Add a task")}),
    )


class TaskMarkDoneForm(forms.Form):
    """Form for handling task mark done actions."""

    done = forms.BooleanField(required=False)

    def __init__(self, project: Project, *args: Any, **kwargs: Any) -> None:
        """Initialize form with task choices from project."""
        super().__init__(*args, **kwargs)
        self.fields["task_uuid"] = forms.ModelChoiceField(
            queryset=Task.objects.filter(project=project),
            to_field_name="uuid",
            required=True,
        )


# Factored out of project_detail_view
def _project_detail_view_actions(
    request: AuthenticatedHttpRequest,
    project: Project,
    team_member: TeamMember,
) -> tuple[str, dict[str, Any]]:
    """Handle POST actions for project detail view."""
    template = "workspace/project_detail.html"
    context: dict[str, Any] = {}
    match request.method, request.POST.get("action"):
        case "POST", "quick_add_task":
            form = TaskQuickAddForm(data=request.POST)
            if not form.is_valid():
                raise BadRequest(
                    _(
                        "Task quick create form not valid. Errors={errors}"
                    ).format(errors=form.errors)
                )
            t = form.cleaned_data["title"]
            task_create(who=request.user, project=project, title_description=t)
            template = "workspace/project_detail.html#project_tasks"
        case "POST", "mark_task_done":
            task_mark_done_form = TaskMarkDoneForm(
                project=project, data=request.POST
            )
            if not task_mark_done_form.is_valid():
                raise BadRequest()
            task = task_mark_done_form.cleaned_data["task_uuid"]
            task_mark_done(
                who=request.user,
                task=task,
                done=task_mark_done_form.cleaned_data["done"],
            )
            template = "workspace/project_detail.html#project_tasks"
        case "POST", "minimize_team_member_filter":
            team_member_minimize_team_member_filter(
                team_member=team_member,
                minimized=request.POST.get("team_member_filter_minimized")
                == "true",
            )
            template = "workspace/common/sidemenu/project_details.html"
        case "POST", action:
            raise BadRequest(
                _("Unrecognized action '{action}'").format(action=action)
            )
        case _:
            pass

    return template, context


# HTML
@require_http_methods(["GET", "POST"])
@platform_view
def project_detail_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Show project details."""
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))

    team_member = team_member_find_for_workspace(
        user=request.user, workspace=project.workspace
    )
    if team_member is None:
        raise RuntimeError("No team member")

    qs = project_detail_query_set(who=request.user)

    template, context = _project_detail_view_actions(
        request, project, team_member
    )

    # TODO run this before the match: case:
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=qs
    )
    assert project, "Project disappeared"

    # Mark this project as most recently visited
    team_member_visit_project(team_member=team_member, project=project)

    project.workspace.quota = workspace_get_all_quotas(project.workspace)
    team_members = project.workspace.teammember_set.all()

    context = {
        **context,
        **get_project_view_context(request, project.workspace),
        "project_description": strip_first_paragraph(
            project.description or ""
        ),
        "project": project,
        "team_members": team_members,
        "quick_add_task": TaskQuickAddForm(),
    }
    return render(request, template, context)


class ProjectForm(forms.Form):
    """Form for project creation."""

    description = forms.CharField(
        label=_("Description"),
        widget=RichTextEditor(
            heading_blocks=False,
            attrs={"expand": True, "class": TASK_EDITOR_MIN_HEIGHT_CLASS},
        ),
    )

    def __init__(self, *args: Any, workspace: Workspace, **kwargs: Any):
        """Populate available assignees and optionally set autofocus."""
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["data-suggest-links-url"] = (
            reverse(
                "dashboard:workspaces:suggest-links-task",
                args=(workspace.uuid,),
            )
        )
        self.fields["description"].widget.attrs[
            "data-suggest-projects-url"
        ] = reverse(
            "dashboard:workspaces:suggest-links-project",
            args=(workspace.uuid,),
        )


@require_http_methods(["GET", "POST"])
@platform_view
def project_create_view(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Create a new project in a workspace."""
    qs: Optional[QuerySet[Workspace]]
    match request.method:
        case "GET":
            qs = workspace_build_detail_query_set(who=request.user)
        case "POST":
            qs = None
        case other:
            # Should never be hit
            assert False, other
    workspace = workspace_find_by_workspace_uuid(
        workspace_uuid=workspace_uuid, who=request.user, qs=qs
    )
    if workspace is None:
        raise Http404(_("No workspace found for this UUID"))

    if request.method == "GET":
        context = {
            **get_project_view_context(request, workspace),
            "form": ProjectForm(workspace=workspace),
        }
        return render(request, "workspace/project_create.html", context)

    form = ProjectForm(request.POST, workspace=workspace)
    if not form.is_valid():
        context = {
            **get_project_view_context(request, workspace),
            "form": form,
        }
        return render(
            request, "workspace/project_create.html", context, status=400
        )

    try:
        project: Project = project_create(
            title_description=form.cleaned_data["description"],
            due_date=form.cleaned_data.get("due_date"),
            who=request.user,
            workspace=workspace,
        )
        return redirect("dashboard:projects:detail", project_uuid=project.uuid)
    except ValidationError as error:
        populate_form_with_errors(form, error)
        context = {
            **get_project_view_context(request, workspace),
            "form": form,
        }
        return render(
            request, "workspace/project_create.html", context, status=400
        )


@require_http_methods(["GET", "POST"])
@platform_view
def project_update_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Update an existing project."""
    qs: Optional[QuerySet[Project]]
    match request.method:
        case "GET":
            qs = project_detail_query_set(who=request.user)
        case "POST":
            qs = None
        case other:
            assert False, other
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=qs
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))

    workspace = project.workspace
    context = {
        **get_project_view_context(request, workspace),
        "project": project,
        "workspace": workspace,
    }

    if request.method == "GET":
        form = ProjectForm(
            workspace=workspace, initial={"description": project.description}
        )
        context = {"form": form, **context}
        return render(request, "workspace/project_update.html", context)

    form = ProjectForm(data=request.POST, workspace=workspace)
    if not form.is_valid():
        context = {"form": form, **context}
        return render(
            request, "workspace/project_update.html", context, status=400
        )

    try:
        project_update(
            who=request.user,
            project=project,
            title_description=form.cleaned_data["description"],
        )
        return redirect(project.get_absolute_url())
    except ValidationError as error:
        populate_form_with_errors(form, error)
        context = {"form": form, **context}
        return render(
            request, "workspace/project_update.html", context, status=400
        )


@require_http_methods(["POST"])
@platform_view
def project_archive_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Archive a project via HTMX."""
    assert request.method == "POST"
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, archived=False
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))
    project_archive(project=project, archived=True, who=request.user)
    return HttpResponseClientRefresh()


@require_http_methods(["POST"])
@platform_view
def project_recover_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Recover an archived project via HTMX."""
    assert request.method == "POST"

    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, archived=True
    )
    if project is None:
        raise Http404(_("No archived project found for this uuid"))

    project_archive(project=project, archived=False, who=request.user)
    return HttpResponseClientRefresh()


@require_http_methods(["POST"])
@platform_view
def project_delete_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Delete an archived project via HTMX."""
    assert request.method == "POST"

    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, archived=True
    )
    if project is None:
        raise Http404(_("No archived project found for this uuid"))

    project_delete(project=project, who=request.user)
    return HttpResponseClientRefresh()
