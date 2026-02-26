# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Task CRUD views."""

import logging
from typing import Any, Literal, Optional
from uuid import UUID

from django import forms
from django.core.exceptions import BadRequest
from django.forms.formsets import TOTAL_FORM_COUNT
from django.http import HttpResponse, QueryDict
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST

from projectify.lib.htmx import HttpResponseClientRedirect
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.selectors.team_member import (
    team_member_find_for_workspace,
)

from ..models.task import Task
from ..models.workspace import Workspace
from ..selectors.section import (
    SectionDetailQuerySet,
    section_find_for_user_and_uuid,
)
from ..selectors.task import TaskDetailQuerySet, task_find_by_task_uuid
from ..selectors.workspace import workspace_find_for_user
from ..services.sub_task import ValidatedDatum, ValidatedDatumWithUuid
from ..services.task import (
    task_create_nested,
    task_delete,
    task_move_after,
    task_move_in_direction,
    task_update_nested,
)

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


class TaskCreateForm(forms.Form):
    """Form for task creation."""

    template_name_table = "workspace/forms/table.html"

    title = forms.CharField(
        label=_("Task title"),
        widget=forms.TextInput(attrs={"placeholder": _("Task title")}),
    )
    due_date = forms.DateTimeField(
        required=False,
        label=_("Due date"),
        widget=forms.DateTimeInput(attrs={"type": "date"}),
    )
    description = forms.CharField(
        required=False,
        label=_("Description"),
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description for your task")}
        ),
    )

    def __init__(self, workspace: Workspace, *args: Any, **kwargs: Any):
        """Populate available assignees and labels."""
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

        labels_widget = forms.CheckboxSelectMultiple()
        labels_widget.option_template_name = (
            "workspace/forms/widgets/select_label_option.html"
        )
        self.fields["labels"] = forms.ModelMultipleChoiceField(
            required=False,
            blank=True,
            label=_("Labels"),
            queryset=workspace.label_set.all(),
            widget=labels_widget,
            to_field_name="uuid",
        )

        self.order_fields(
            ["title", "assignee", "labels", "due_date", "description"]
        )


class TaskCreateSubTaskForm(forms.Form):
    """Form for creating sub tasks as part of task creation."""

    title = forms.CharField(label=_("Sub task title"))
    done = forms.BooleanField(required=False, label=_("Done"))


TaskCreateSubTaskForms = forms.formset_factory(TaskCreateSubTaskForm, extra=0)  # type: ignore[type-var]


class TaskUpdateSubTaskForm(forms.Form):
    """Form for creating sub tasks as part of task creation."""

    title = forms.CharField(required=False, label=_("Sub task title"))
    done = forms.BooleanField(required=False, label=_("Done"))
    uuid = forms.UUIDField(required=False, widget=forms.HiddenInput)
    delete = forms.BooleanField(
        required=False,
        label=_("Delete task"),
        initial=False,
    )


class TaskUpdateSubTaskFormSet(forms.BaseFormSet):  # type:ignore[type-arg]
    """Custom formset for task update sub tasks with focus mechanism."""

    def __init__(
        self,
        focus_subtask_uuid: Optional[UUID] = None,
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize formset with optional focus on specific subtask."""
        super().__init__(*args, **kwargs)

        if not focus_subtask_uuid:
            return
        if not self.forms:
            return
        for form in self.forms:
            if form.initial and form.initial.get("uuid") == focus_subtask_uuid:
                break
        else:
            logger.warning(
                "Couldn't find sub task %s in formset", focus_subtask_uuid
            )
            return
        form.fields["title"].widget.attrs["autofocus"] = True


TaskUpdateSubTaskForms = forms.formset_factory(
    TaskUpdateSubTaskForm, formset=TaskUpdateSubTaskFormSet, extra=0
)


@platform_view
def task_create_sub_task_form(
    request: AuthenticatedHttpRequest,
    sub_tasks: int,
) -> HttpResponse:
    """Return a single form for a sub task."""
    formset = TaskCreateSubTaskForms().empty_form
    formset.prefix = f"form-{sub_tasks}"
    new_sub_tasks = sub_tasks + 1
    return render(
        request,
        "workspace/task_create/sub_task.html",
        {"empty_formset": formset, "formset_total": new_sub_tasks},
    )


@platform_view
@require_http_methods(["GET", "POST"])
def task_create(
    request: AuthenticatedHttpRequest, section_uuid: UUID
) -> HttpResponse:
    """Create a task. Render form error if unsuccessful."""
    section = section_find_for_user_and_uuid(
        user=request.user, section_uuid=section_uuid, qs=SectionDetailQuerySet
    )
    if section is None:
        raise Http404(_("Section not found"))

    workspace = section.project.workspace
    context: dict[str, Any] = {
        **get_task_view_context(request, workspace),
        "section": section,
    }

    match request.method:
        case "GET":
            return render(
                request,
                "workspace/task_create.html",
                {
                    **context,
                    "form": TaskCreateForm(workspace=workspace),
                    "formset": TaskCreateSubTaskForms(),
                },
            )
        case "POST":
            pass
        case method:
            raise RuntimeError(f"Don't know how to handle method {method}")
    form = TaskCreateForm(workspace, request.POST)
    formset = TaskCreateSubTaskForms(request.POST.dict())
    all_valid = form.is_valid() and formset.is_valid()
    if not formset.is_valid():
        logger.warning("Formset validation errors: %s", formset.errors)
    if not all_valid:
        return render(
            request,
            "workspace/task_create.html",
            {**context, "form": form, "formset": formset},
            status=400,
        )

    sub_tasks: list[ValidatedDatum] = [
        {"title": d["title"], "done": d["done"], "_order": i}
        for i, d in enumerate(formset.cleaned_data)
        if d.get("title")
    ]

    task = task_create_nested(
        who=request.user,
        section=section,
        title=form.cleaned_data["title"],
        description=form.cleaned_data.get("description"),
        assignee=form.cleaned_data.get("assignee"),
        due_date=form.cleaned_data.get("due_date"),
        labels=form.cleaned_data["labels"],
        sub_tasks={"create_sub_tasks": sub_tasks, "update_sub_tasks": []},
    )

    match request.POST.get("action"):
        case "create_stay":
            return redirect("dashboard:tasks:detail", task.uuid)
        case "create":
            return redirect(section.get_absolute_url())
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
        "project": task.section.project,
    }
    # TODO map sub task progress to 20 piece 5 % increment w-[X%] tailwind
    # classes to solve CSP issue
    return render(request, "workspace/task_detail.html", context)


class TaskUpdateForm(forms.Form):
    """Form for task creation."""

    template_name_table = "workspace/forms/table.html"

    title = forms.CharField(
        label=_("Task title"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Task title")},
        ),
    )
    due_date = forms.DateTimeField(
        required=False,
        label=_("Due date"),
        widget=forms.DateTimeInput(attrs={"type": "date"}),
    )
    description = forms.CharField(
        required=False,
        label=_("Description"),
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description for your task")}
        ),
    )

    def __init__(
        self,
        *args: Any,
        workspace: Workspace,
        focus_field: Optional[str],
        **kwargs: Any,
    ):
        """Populate available assignees and set autofocus."""
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

        labels_widget = forms.CheckboxSelectMultiple()
        labels_widget.option_template_name = (
            "workspace/forms/widgets/select_label_option.html"
        )
        self.fields["labels"] = forms.ModelMultipleChoiceField(
            required=False,
            blank=True,
            label=_("Labels"),
            queryset=workspace.label_set.all(),
            widget=labels_widget,
            to_field_name="uuid",
        )

        self.order_fields(
            ["title", "assignee", "labels", "due_date", "description"]
        )

        if focus_field is None:
            return
        if focus_field in self.fields:
            self.fields[focus_field].widget.attrs["autofocus"] = True
        else:
            logger.warning(
                "Couldn't find focus_field=%s in self.fields", focus_field
            )


class TaskUpdateFocusForm(forms.Form):
    """Form for parsing focus field and subtask UUID from query parameters."""

    focus = forms.CharField(required=False)
    subtask_uuid = forms.UUIDField(required=False)


@platform_view
@require_http_methods(["GET", "POST"])
def task_update_view(
    request: AuthenticatedHttpRequest, task_uuid: UUID
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

    focus_form = TaskUpdateFocusForm(request.GET)
    focus_field: Optional[str] = None
    subtask_uuid: Optional[UUID] = None
    if not focus_form.is_valid():
        raise BadRequest("Invalid form data for update focus form")
    focus_field = focus_form.cleaned_data.get("focus")
    subtask_uuid = focus_form.cleaned_data.get("subtask_uuid")

    workspace = task.workspace
    context: dict[str, Any] = get_task_view_context(request, workspace)
    task_initial = {
        "title": task.title,
        "assignee": task.assignee,
        "labels": task.labels.all(),
        "due_date": task.due_date,
        "description": task.description,
    }
    sub_tasks = task.subtask_set.all()
    sub_tasks_initial = [
        {"title": sub_task.title, "done": sub_task.done, "uuid": sub_task.uuid}
        for sub_task in sub_tasks
    ]

    # Determine what update view action should be taken
    match request.method, request.POST.get("action"):
        case "POST", "update":
            next_url = reverse(
                "dashboard:projects:detail", args=(task.section.project.uuid,)
            )
        case "POST", "update_stay":
            next_url = reverse("dashboard:tasks:detail", args=(task.uuid,))
        case "POST", "add_sub_task":
            post: QueryDict = request.POST.copy()
            sub_task_count_raw: str = post.get("form-" + TOTAL_FORM_COUNT, "0")
            try:
                sub_task_count = int(sub_task_count_raw)
            except ValueError as e:
                logger.error(
                    "Unexpected error when getting total form count",
                    exc_info=e,
                )
                sub_task_count = 0
            post["form-TOTAL_FORMS"] = str(sub_task_count + 1)
            logger.info("Adding sub task")
            form = TaskUpdateForm(
                data=post, workspace=workspace, focus_field=focus_field
            )
            formset = TaskUpdateSubTaskForms(data=post)  # type: ignore[arg-type]
            context = {
                **context,
                "form": form,
                "task": task,
                "formset": formset,
            }
            return render(request, "workspace/task_update.html", context)
        case "GET", _:
            form = TaskUpdateForm(
                initial=task_initial,
                workspace=workspace,
                focus_field=focus_field,
            )
            formset = TaskUpdateSubTaskForms(
                subtask_uuid,
                initial=sub_tasks_initial,  # type: ignore[arg-type]
            )
            context = {
                **context,
                "form": form,
                "task": task,
                "formset": formset,
            }
            logger.warning("No action specified")
            next_url = reverse(
                "dashboard:projects:detail", args=(task.section.project.uuid,)
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

    form = TaskUpdateForm(
        data=request.POST.copy(),
        initial=task_initial,
        workspace=workspace,
        focus_field=focus_field,
    )
    form.full_clean()
    formset = TaskUpdateSubTaskForms(
        data=request.POST,  # type: ignore[arg-type]
        initial=sub_tasks_initial,  # type: ignore[arg-type]
    )
    formset.full_clean()
    if not form.is_valid() or not formset.is_valid():
        logger.warning(
            "form.is_valid=%s, formset.is_valid()=%s",
            form.is_valid(),
            formset.is_valid(),
        )
        context = {**context, "form": form, "task": task, "formset": formset}
        return render(
            request, "workspace/task_update.html", context, status=400
        )

    cleaned_data = form.cleaned_data
    formset_cleaned_data = formset.cleaned_data
    update_sub_tasks: list[ValidatedDatumWithUuid] = [
        {
            "title": f["title"],
            "done": f["done"],
            "_order": i,
            "uuid": f["uuid"],
        }
        for i, f in enumerate(formset_cleaned_data)
        if f and f["uuid"] and not f["delete"]
    ]
    create_sub_tasks: list[ValidatedDatum] = [
        {
            "title": f["title"],
            "done": f["done"],
            "_order": i,
        }
        for i, f in enumerate(formset_cleaned_data)
        # Only include sub tasks that have a title
        if f and not f["uuid"] and not f["delete"] and f["title"].strip()
    ]
    task_update_nested(
        who=request.user,
        task=task,
        title=cleaned_data["title"],
        description=cleaned_data["description"],
        due_date=cleaned_data["due_date"],
        assignee=cleaned_data["assignee"],
        labels=cleaned_data["labels"],
        sub_tasks={
            "update_sub_tasks": update_sub_tasks,
            "create_sub_tasks": create_sub_tasks,
        },
    )
    return redirect(next_url)


# Form
class TaskMoveForm(forms.Form):
    """Form that captures which direction to move a task."""

    direction = forms.ChoiceField(
        choices=[
            ("top", _("Top")),
            ("up", _("Up")),
            ("down", _("Down")),
            ("bottom", _("Bottom")),
        ]
    )


@require_POST
def task_move(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Move a task depending on form input."""
    task = get_object(request, task_uuid)
    form = TaskMoveForm(request.POST)
    if not form.is_valid():
        # TODO
        return HttpResponse(status=400)
    direction: Literal["up", "down", "top", "bottom"]
    dir_in: str = form.cleaned_data["direction"]
    match dir_in:
        case "up" | "down" | "top" | "bottom":
            direction = dir_in
        case _:
            # TODO
            raise Exception(f"Did not recognize direction {dir_in}")

    task = task_move_in_direction(
        who=request.user, task=task, direction=direction
    )

    return redirect("dashboard:projects:detail", task.section.project.uuid)


class TaskMoveToSectionForm(forms.Form):
    """Form that captures which section to move a task to."""

    section_uuid = forms.UUIDField()


@require_POST
def task_move_to_section(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Move a task to a given section."""
    task = get_object(request, task_uuid)
    form = TaskMoveToSectionForm(request.POST)
    if not form.is_valid():
        logger.warning("Form not valid for task_uuid %s", task_uuid)
        # TODO
        return HttpResponse(status=400)
    section_uuid = form.cleaned_data["section_uuid"]
    section = section_find_for_user_and_uuid(
        user=request.user, section_uuid=section_uuid
    )
    if section is None:
        logger.warning("Section with uuid %s not found", section_uuid)
        # TODO give better validation message when section not found
        return HttpResponse(status=400)
    task = task_move_after(who=request.user, task=task, after=section)

    return redirect("dashboard:projects:detail", task.section.project.uuid)


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
        "sections": task.section.project.section_set.all(),
        "project": task.section.project,
    }
    return render(request, "workspace/task_actions.html", context)


def task_delete_view(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Delete task."""
    task = get_object(request, task_uuid)
    task_delete(who=request.user, task=task)
    return HttpResponseClientRedirect(task.section.get_absolute_url())
