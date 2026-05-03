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
        label=_("Task description"),
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

        if focus_field is None:
            return
        if focus_field in self.fields:
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
    context: dict[str, Any] = {
        **get_task_view_context(request, workspace),
        "project": project,
    }

    match request.method:
        case "GET":
            return render(
                request,
                "workspace/task_create.html",
                {
                    **context,
                    "form": TaskForm(
                        workspace=workspace, initial={"project": project}
                    ),
                },
            )
        case "POST":
            pass
        case method:
            raise RuntimeError(f"Don't know how to handle method {method}")
    form = TaskForm(workspace=workspace, data=request.POST)
    if not form.is_valid():
        return render(
            request,
            "workspace/task_create.html",
            {**context, "form": form},
            status=400,
        )

    task = task_create(
        who=request.user,
        project=project,
        title_description=form.cleaned_data["description"],
        assignee=form.cleaned_data.get("assignee"),
        due_date=form.cleaned_data.get("due_date"),
    )

    match request.POST.get("action"):
        case "create_stay":
            return redirect("dashboard:tasks:detail", task.uuid)
        case "create":
            return redirect(project)
        case action:
            raise BadRequest(
                _("Invalid action: {action}").format(action=action)
            )


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
    context: dict[str, Any] = {
        **get_task_view_context(request, workspace),
        "project": task.project,
    }
    task_initial = {
        "assignee": task.assignee,
        "due_date": task.due_date,
        "description": task.description,
        "project": task.project,
    }

    # Determine what update view action should be taken
    match request.method, request.POST.get("action"):
        case "POST", "update":
            next_url = reverse(
                "dashboard:projects:detail", args=(task.project.uuid,)
            )
        case "POST", "update_stay":
            next_url = reverse("dashboard:tasks:detail", args=(task.uuid,))
        case "GET", _:
            form = TaskForm(
                initial=task_initial,
                workspace=workspace,
                focus_field=focus_field,
            )
            context = {**context, "form": form, "task": task}
            logger.warning("No action specified")
            next_url = reverse(
                "dashboard:projects:detail", args=(task.project.uuid,)
            )
            return render(request, "workspace/task_update.html", context)
        case method, other_action:
            raise BadRequest(
                _(
                    "Invalid method {method} and action {action}".format(
                        method=method, action=other_action
                    )
                )
            )

    form = TaskForm(
        data=request.POST.copy(),
        initial=task_initial,
        workspace=workspace,
        focus_field=focus_field,
    )
    form.full_clean()
    if not form.is_valid():
        context = {**context, "form": form, "task": task}
        return render(
            request, "workspace/task_update.html", context, status=400
        )

    cleaned_data = form.cleaned_data
    task_update(
        who=request.user,
        task=task,
        title_description=cleaned_data["description"],
        due_date=cleaned_data["due_date"],
        assignee=cleaned_data["assignee"],
    )
    return redirect(next_url)


# Form


def task_actions(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Render task actions menu page."""
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

    if request.htmx:
        template = "workspace/task_actions.html#tr_dropdown"
    else:
        template = "workspace/task_actions.html"
    return render(request, template, context)


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
