# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2026 JWP Consulting GK
"""Task CRUD views."""

import logging
from typing import Any, Optional
from uuid import UUID

from django import forms
from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from projectify.lib.forms import RichTextEditor
from projectify.lib.htmx import (
    HttpResponseClientRedirect,
    HttpResponseClientRefresh,
)
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.selectors.project import (
    ProjectDetailQuerySet,
    project_find_by_project_uuid,
)

from ..const import TASK_EDITOR_MIN_HEIGHT_CLASS
from ..models import Task, Workspace
from ..selectors.task import TaskDetailQuerySet, task_find_by_task_uuid
from ..selectors.team_member import team_member_find_for_workspace
from ..selectors.workspace import workspace_find_for_user
from ..services.task import task_create, task_delete, task_update

logger = logging.getLogger(__name__)


def get_object(request: AuthenticatedHttpRequest, task_uuid: UUID) -> Task:
    """Get object for user and uuid."""
    user = request.user
    obj = task_find_by_task_uuid(
        # TODO TaskDetailQuerySet probably not needed
        # Remove when DRF views are gone
        who=user,
        task_uuid=task_uuid,
        qs=TaskDetailQuerySet,
    )
    if obj is None:
        raise Http404(
            _("Task with uuid {task_uuid} not found").format(
                task_uuid=task_uuid
            )
        )
    return obj


def get_task_view_context(
    request: AuthenticatedHttpRequest, workspace: Workspace
) -> dict[str, Any]:
    """Return context with workspace, workspaces and current_team_member_qs."""
    return {
        "workspace": workspace,
        "workspaces": workspace_find_for_user(who=request.user),
        "projects": workspace.project_set.all(),
        "current_team_member_qs": team_member_find_for_workspace(
            user=request.user, workspace=workspace
        ),
    }


class TaskForm(forms.Form):
    """Base form for task creation and update."""

    due_date = forms.DateTimeField(
        required=False,
        label=_("Due date"),
        widget=forms.DateTimeInput(attrs={"type": "date"}),
    )
    description = forms.CharField(
        label=_("Description"),
        widget=RichTextEditor(
            heading_blocks=False,
            attrs={
                "expand": True,
                "placeholder": _("Enter a description for your task"),
                "class": TASK_EDITOR_MIN_HEIGHT_CLASS,
            },
        ),
    )

    def __init__(
        self,
        *args: Any,
        workspace: Workspace,
        focus_field: Optional[str] = None,
        **kwargs: Any,
    ):
        """Populate available assignees and optionally set autofocus."""
        super().__init__(*args, **kwargs)
        assignee_widget = forms.RadioSelect()
        assignee_widget.option_template_name = (
            "workspace/forms/widgets/select_team_member_option.html"
        )
        self.fields["assignee"] = forms.ModelChoiceField(
            required=False,
            blank=True,
            label=_("Assignee"),
            queryset=workspace.teammember_set.all(),
            widget=assignee_widget,
            to_field_name="uuid",
            empty_label=_("Assigned to nobody"),
        )
        self.order_fields(["description", "assignee", "due_date"])

        self.fields["description"].widget.attrs["data-suggest-links-url"] = (
            reverse(
                "dashboard:workspaces:suggest-links", args=(workspace.uuid,)
            )
        )

        if focus_field is None:
            pass
        elif focus_field in self.fields:
            self.fields[focus_field].widget.attrs["autofocus"] = True
        else:
            logger.warning(
                "Couldn't find focus_field=%s in self.fields", focus_field
            )


@platform_view
@require_http_methods(["GET", "POST"])
def task_create_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Create a task. Render form error if unsuccessful."""
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=ProjectDetailQuerySet
    )
    if project is None:
        raise Http404(_("Project not found"))
    workspace = project.workspace
    match request.method:
        case "GET":
            form = TaskForm(workspace=workspace, initial={"project": project})
            status = 200
        case "POST":
            form = TaskForm(workspace=workspace, data=request.POST)
            if form.is_valid():
                task_create(
                    who=request.user,
                    project=project,
                    title_description=form.cleaned_data["description"],
                    assignee=form.cleaned_data.get("assignee"),
                    due_date=form.cleaned_data.get("due_date"),
                )
                return redirect(project)
            else:
                status = 400
        case method:
            raise RuntimeError(f"Don't know how to handle method {method}")
    context = {
        **get_task_view_context(request, workspace),
        "project": project,
        "form": form,
    }
    template = "workspace/task_create.html"
    return render(request, template, context, status=status)


@platform_view
def task_detail(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """View a task. Accept POST for task updates."""
    task = task_find_by_task_uuid(
        who=request.user, task_uuid=task_uuid, qs=TaskDetailQuerySet
    )
    if task is None:
        raise Http404(
            _("Could not find task with uuid {task_uuid}").format(
                task_uuid=task_uuid
            )
        )

    workspace = task.workspace

    context = {
        **get_task_view_context(request, workspace),
        "task": task,
        "project": task.project,
    }

    # If HTMX request, return just the panel content
    if request.htmx:
        template = "workspace/task_detail.html#task_inline"
    else:
        template = "workspace/task_detail.html"
    return render(request, template, context)


@platform_view
@require_http_methods(["GET", "POST"])
def task_update_view(
    request: AuthenticatedHttpRequest,
    task_uuid: UUID,
    focus_field: Optional[str] = None,
) -> HttpResponse:
    """Update task. Render errors."""
    task = task_find_by_task_uuid(
        who=request.user, task_uuid=task_uuid, qs=TaskDetailQuerySet
    )
    if task is None:
        raise Http404(
            _("Could not find task with uuid {task_uuid}").format(
                task_uuid=task_uuid
            )
        )

    workspace = task.workspace
    task_initial = {
        "assignee": task.assignee,
        "due_date": task.due_date,
        "description": task.description,
        "project": task.project,
    }
    match request.method:
        case "GET":
            form = TaskForm(
                initial=task_initial,
                workspace=workspace,
                focus_field=focus_field,
            )
            status = 200
        case "POST":
            form = TaskForm(
                data=request.POST,
                initial=task_initial,
                workspace=workspace,
                focus_field=focus_field,
            )
            form.full_clean()
            if form.is_valid():
                task_update(
                    who=request.user,
                    task=task,
                    title_description=form.cleaned_data["description"],
                    due_date=form.cleaned_data["due_date"],
                    assignee=form.cleaned_data["assignee"],
                )
                return redirect(task.get_absolute_url())
            else:
                status = 400
        case method:
            raise BadRequest(
                _("Invalid method {method}").format(method=method)
            )
    context = {
        **get_task_view_context(request, workspace),
        "project": task.project,
        "form": form,
        "task": task,
    }
    template = "workspace/task_update.html"
    return render(request, template, context, status=status)


# TODO require POST
def task_delete_view(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Delete task."""
    task = get_object(request, task_uuid)
    project = task.project
    task_delete(who=request.user, task=task)
    if request.htmx.current_url and "/task/" in request.htmx.current_url:
        return HttpResponseClientRedirect(project.get_absolute_url())
    else:
        return HttpResponseClientRefresh()
