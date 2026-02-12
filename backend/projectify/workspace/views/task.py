# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Task CRUD views."""

import logging
from typing import Any, Literal, Optional, Union
from uuid import UUID

from django import forms
from django.core.exceptions import BadRequest
from django.forms.formsets import TOTAL_FORM_COUNT
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.htmx import HttpResponseClientRedirect
from projectify.lib.schema import extend_schema
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view

from ..models.label import Label
from ..models.section import Section
from ..models.task import Task
from ..models.workspace import Workspace
from ..selectors.section import (
    SectionDetailQuerySet,
    section_find_for_user_and_uuid,
)
from ..selectors.task import TaskDetailQuerySet, task_find_by_task_uuid
from ..selectors.workspace import workspace_find_for_user
from ..serializers.task_detail import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskUpdateSerializer,
)
from ..services.sub_task import (
    ValidatedData,
    ValidatedDatum,
    ValidatedDatumWithUuid,
)
from ..services.task import (
    task_create_nested,
    task_delete,
    task_move_after,
    task_move_in_direction,
    task_update_nested,
)

logger = logging.getLogger(__name__)


def get_object(
    request: Union[Request, AuthenticatedHttpRequest], task_uuid: UUID
) -> Task:
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
        raise NotFound(
            _("Task with uuid {task_uuid} not found").format(
                task_uuid=task_uuid
            )
        )
    return obj


class TaskCreateForm(forms.Form):
    """Form for task creation."""

    template_name_table = "workspace/forms/table.html"

    title = forms.CharField(
        label=_("Task title"),
        widget=forms.TextInput(attrs={"placeholder": _("Task title")}),
    )
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "date"}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description for your task")}
        ),
    )

    def __init__(self, workspace: Workspace, *args: Any, **kwargs: Any):
        """Populate available assignees and labels."""
        super().__init__(*args, **kwargs)
        assignee_widget = forms.RadioSelect()
        assignee_widget.option_template_name = (
            "workspace/forms/widgets/select_assignee_option.html"
        )
        self.fields["assignee"] = forms.ModelChoiceField(
            required=False,
            blank=True,
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
            queryset=workspace.label_set.all(),
            widget=labels_widget,
            to_field_name="uuid",
        )

        self.order_fields(
            ["title", "assignee", "labels", "due_date", "description"]
        )


class TaskCreateSubTaskForm(forms.Form):
    """Form for creating sub tasks as part of task creation."""

    title = forms.CharField()
    done = forms.BooleanField(required=False)


TaskCreateSubTaskForms = forms.formset_factory(TaskCreateSubTaskForm, extra=0)  # type: ignore[type-var]


class TaskUpdateSubTaskForm(forms.Form):
    """Form for creating sub tasks as part of task creation."""

    title = forms.CharField()
    done = forms.BooleanField(required=False)
    uuid = forms.UUIDField(required=False, widget=forms.HiddenInput)
    delete = forms.BooleanField(
        required=False,
        label=_("Delete task"),
        initial=False,
    )


TaskUpdateSubTaskForms = forms.formset_factory(TaskUpdateSubTaskForm, extra=0)  # type: ignore[type-var]


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
    context: dict[str, Any] = {
        "section": section,
        "projects": section.project.workspace.project_set.all(),
        "workspace": section.project.workspace,
        "workspaces": workspace_find_for_user(who=request.user),
    }
    match request.method:
        case "GET":
            return render(
                request,
                "workspace/task_create.html",
                {
                    **context,
                    "form": TaskCreateForm(
                        workspace=section.project.workspace
                    ),
                    "formset": TaskCreateSubTaskForms(),
                },
            )
        case "POST":
            pass
        case method:
            raise RuntimeError(f"Don't know how to handle method {method}")
    form = TaskCreateForm(section.project.workspace, request.POST)
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
            raise BadRequest(_("Invalid action: {}").format(action))


@platform_view
def task_detail(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """View a task. Accept POST for task updates."""
    task = task_find_by_task_uuid(
        who=request.user, task_uuid=task_uuid, qs=TaskDetailQuerySet
    )
    if task is None:
        raise Http404(_(f"Could not find task with uuid {task_uuid}"))
    context = {
        "task": task,
        "project": task.section.project,
        "workspace": task.workspace,
        "projects": task.workspace.project_set.all(),
        "workspaces": workspace_find_for_user(who=request.user),
    }
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
        widget=forms.DateTimeInput(attrs={"type": "date"}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description for your task")}
        ),
    )
    action = forms.CharField(required=True, widget=forms.HiddenInput())

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
            "workspace/forms/widgets/select_assignee_option.html"
        )
        self.fields["assignee"] = forms.ModelChoiceField(
            required=False,
            blank=True,
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


def determine_action(
    request: AuthenticatedHttpRequest,
) -> Optional[Literal["get", "update", "update_stay", "add_sub_task"]]:
    """Determine what update view action should be taken."""
    if request.method == "GET":
        return "get"
    action: Optional[str] = request.POST.get("action")
    match action:
        case "update":
            return "update"
        case "update_stay":
            return "update_stay"
        case "add_sub_task":
            return "add_sub_task"
        case _:
            return None


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
        raise Http404(_(f"Could not find task with uuid {task_uuid}"))

    focus_field = request.GET.get("focus", None)
    context: dict[str, Any] = {
        "workspace": task.workspace,
        "projects": task.workspace.project_set.all(),
        "workspaces": workspace_find_for_user(who=request.user),
    }

    action = determine_action(request)
    match action:
        case "add_sub_task":
            post: dict[str, Any] = request.POST.dict()
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
                data=post, workspace=task.workspace, focus_field=focus_field
            )
            formset = TaskUpdateSubTaskForms(data=post)
            context = {
                **context,
                "form": form,
                "task": task,
                "formset": formset,
            }
            return render(request, "workspace/task_update.html", context)
        case _:
            pass

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
    if action == "get":
        form = TaskUpdateForm(
            initial=task_initial,
            workspace=task.workspace,
            focus_field=focus_field,
        )
        formset = TaskUpdateSubTaskForms(initial=sub_tasks_initial)  # type: ignore[arg-type]
        # Add autofocus to first subtask if focus_field is subtasks
        if focus_field == "subtasks" and formset.forms:
            formset.forms[0].fields["title"].widget.attrs["autofocus"] = True
        context = {**context, "form": form, "task": task, "formset": formset}
        return render(request, "workspace/task_update.html", context)

    form = TaskUpdateForm(
        data=request.POST,
        initial=task_initial,
        workspace=task.workspace,
        focus_field=focus_field,
    )
    form.full_clean()
    formset = TaskUpdateSubTaskForms(
        data=request.POST.dict(),
        initial=sub_tasks_initial,  # type: ignore[arg-type]
    )
    formset.full_clean()
    if not form.is_valid() or not formset.is_valid():
        context = {**context, "form": form, "task": task, "formset": formset}
        return render(request, "workspace/task_update.html", context)

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
        if f and not f["uuid"] and not f["delete"]
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
    match action:
        case "update_stay":
            n = reverse("dashboard:tasks:detail", args=(task.uuid,))
        case "update":
            n = reverse(
                "dashboard:projects:detail", args=(task.section.project.uuid,)
            )
        case _:
            logger.warning("No action specified")
            n = reverse(
                "dashboard:projects:detail", args=(task.section.project.uuid,)
            )
    return redirect(n)


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
    task = get_object(request, task_uuid)
    context = {
        "task": task,
        "workspace": task.workspace,
        "sections": task.section.project.section_set.all(),
        "projects": task.workspace.project_set.all(),
        "project": task.section.project,
        "workspaces": workspace_find_for_user(who=request.user),
    }
    return render(request, "workspace/task_actions.html", context)


def task_delete_view(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Delete task."""
    task = get_object(request, task_uuid)
    task_delete(who=request.user, task=task)
    return HttpResponseClientRedirect(task.section.get_absolute_url())


# Create
class TaskCreate(APIView):
    """Create a task."""

    @extend_schema(
        request=TaskCreateSerializer,
        responses={201: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = TaskCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        section: Section = validated_data["section"]

        sub_tasks: ValidatedData
        if "sub_tasks" in validated_data:
            sub_tasks = validated_data.pop("sub_tasks")
        else:
            sub_tasks = {"create_sub_tasks": [], "update_sub_tasks": []}

        labels: list[Label] = validated_data.pop("labels")
        task = task_create_nested(
            who=request.user,
            section=section,
            title=validated_data["title"],
            description=validated_data.get("description"),
            assignee=validated_data.get("assignee"),
            due_date=validated_data.get("due_date"),
            labels=labels,
            sub_tasks=sub_tasks,
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(
            data=output_serializer.data, status=status.HTTP_201_CREATED
        )


# Read + Update + Delete
class TaskRetrieveUpdateDelete(APIView):
    """Retrieve a task."""

    @extend_schema(
        responses={200: TaskDetailSerializer},
    )
    def get(self, request: Request, task_uuid: UUID) -> Response:
        """Handle GET."""
        instance = get_object(request, task_uuid)
        serializer = TaskDetailSerializer(instance=instance)
        return Response(data=serializer.data)

    @extend_schema(
        request=TaskUpdateSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request, task_uuid: UUID) -> Response:
        """
        Override update behavior. Return using different serializer.

        The idea is that we accept abbreviated nested fields, but return
        the data whole. (ws board section, sub tasks, labels, etc.)
        """
        # Copied from
        # https://github.com/encode/django-rest-framework/blob/d32346bae55f3e4718a185fb60e9f7a28e389c85/rest_framework/mixins.py#L65
        # We probably don't have to get the full object here!
        instance = get_object(request, task_uuid)
        serializer = TaskUpdateSerializer(
            instance,
            data=request.data,
            # Mild code duplication from
            # https://github.com/encode/django-rest-framework/blob/d32346bae55f3e4718a185fb60e9f7a28e389c85/rest_framework/generics.py#L113
            # :)
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        labels: list[Label] = validated_data.pop("labels")

        sub_tasks: ValidatedData
        if "sub_tasks" in validated_data:
            sub_tasks = validated_data.pop("sub_tasks")
        else:
            sub_tasks = {"create_sub_tasks": [], "update_sub_tasks": []}

        task_update_nested(
            who=request.user,
            task=instance,
            title=validated_data["title"],
            description=validated_data.get("description"),
            assignee=validated_data.get("assignee"),
            due_date=validated_data.get("due_date"),
            labels=labels,
            sub_tasks=sub_tasks,
        )

        instance = get_object(request, task_uuid)
        response_serializer = TaskDetailSerializer(instance=instance)
        return Response(
            status=status.HTTP_200_OK, data=response_serializer.data
        )

    @extend_schema(
        responses={204: None},
    )
    def delete(self, request: Request, task_uuid: UUID) -> Response:
        """Delete task."""
        instance = get_object(request, task_uuid)
        task_delete(task=instance, who=self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# RPC
class TaskMoveToSection(APIView):
    """Move a task to the beginning of a section."""

    class TaskMoveToSectionSerializer(serializers.Serializer):
        """Accept the target section uuid."""

        section_uuid = serializers.UUIDField()

    @extend_schema(
        request=TaskMoveToSectionSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.TaskMoveToSectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = task_find_by_task_uuid(who=user, task_uuid=task_uuid)
        if task is None:
            raise NotFound(_("Task for this UUID not found"))
        section = section_find_for_user_and_uuid(
            section_uuid=data["section_uuid"],
            user=user,
        )
        if section is None:
            raise serializers.ValidationError(
                {"section_uuid": _("No section was found for the given uuid")}
            )
        task_move_after(task=task, who=user, after=section)
        task = task_find_by_task_uuid(
            who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


# TODO inaccuracy: Might want to be able to move in front of a given task as
# well
class TaskMoveAfterTask(APIView):
    """Move a task right behind another task."""

    class TaskMoveAfterTaskSerializer(serializers.Serializer):
        """Accept a task uuid after which this task should be moved."""

        task_uuid = serializers.UUIDField()

    @extend_schema(
        request=TaskMoveAfterTaskSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.TaskMoveAfterTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = task_find_by_task_uuid(who=user, task_uuid=task_uuid)
        if task is None:
            raise NotFound(_("Task for this UUID not found"))
        after = task_find_by_task_uuid(task_uuid=data["task_uuid"], who=user)
        if after is None:
            raise serializers.ValidationError(
                {"after_task_uuid": _("No task was found for the given uuid")}
            )
        task_move_after(task=task, who=user, after=after)
        task = task_find_by_task_uuid(
            who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
