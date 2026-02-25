# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Project views."""

import logging
from typing import Any, Optional, TypeVar, Union
from uuid import UUID

from django import forms
from django.core.exceptions import BadRequest
from django.db.models import Model, QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from rest_framework.exceptions import ValidationError

from projectify.lib.forms import populate_form_with_drf_errors
from projectify.lib.htmx import HttpResponseClientRefresh
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view

from ..models import Project, Workspace
from ..models.label import Label
from ..models.section import Section
from ..models.task import Task
from ..models.team_member import TeamMember
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
from ..services.section import section_minimize
from ..services.task import task_move_in_direction
from ..services.team_member import (
    team_member_minimize_label_filter,
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


class ModelMultipleChoiceFieldWithEmpty(forms.ModelMultipleChoiceField):
    """Override ModelMultipleChoiceField and allow empty label."""

    def __init__(self, queryset: QuerySet[Any], **kwargs: Any) -> None:
        """Override init."""
        super(forms.ModelMultipleChoiceField, self).__init__(
            queryset, **kwargs
        )

    def clean(self, value: list[str]) -> tuple[bool, Optional[QuerySet[Any]]]:
        """
        Return a tuple of values.

        The first value is a bool that tells you whether the user selected the blank
        option

        The second value is an optional queryset.
        If no values have been selected, it's empty. If values have been
        selected, it's a queryset.
        """
        has_empty = False
        value_without_empty: list[str] = []
        if len(value) == 0:
            return False, None
        for v in value:
            if len(v) == 0:
                has_empty = True
            else:
                value_without_empty.append(v)
        match value_without_empty:
            case []:
                cleaned = None
            case values:
                cleaned_qs: QuerySet[Any] = super().clean(values)
                if not cleaned_qs.exists():
                    cleaned = None
                else:
                    cleaned = cleaned_qs

        return has_empty, cleaned


class ProjectFilterForm(forms.Form):
    """Form for deserializing project task filters."""

    task_search_query = forms.CharField(
        label=_("Task search"),
        required=False,
        help_text=_("Enter search terms"),
    )

    def __init__(
        self,
        team_members: QuerySet[TeamMember],
        labels: QuerySet[Label],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Populate choices."""
        super().__init__(*args, **kwargs)
        member_widget = forms.CheckboxSelectMultiple(
            attrs={"form": "task-filter"},
        )
        member_widget.option_template_name = (
            "workspace/forms/widgets/select_team_member_option.html"
        )
        self.fields["filter_by_team_member"] = (
            ModelMultipleChoiceFieldWithEmpty(
                required=False,
                blank=True,
                label=_("Filter tasks by team member:"),
                queryset=team_members,
                widget=member_widget,
                to_field_name="uuid",
                empty_label=_("Assigned to nobody"),
            )
        )
        label_widget = forms.CheckboxSelectMultiple(
            attrs={"form": "task-filter"},
        )
        label_widget.option_template_name = (
            "workspace/forms/widgets/select_label_option.html"
        )
        self.fields["filter_by_label"] = ModelMultipleChoiceFieldWithEmpty(
            required=False,
            blank=True,
            label=_("Filter tasks by label:"),
            queryset=labels,
            widget=label_widget,
            to_field_name="uuid",
            empty_label=_("No label"),
        )

    def clean(self) -> dict[str, Any]:
        """Override clean and make empty fields None instead."""
        data = super().clean()
        if data["task_search_query"] == "":
            data["task_search_query"] = None
        return data


class SectionMinimizeForm(forms.Form):
    """Form for handling section minimize actions."""

    action = forms.CharField(required=True)
    minimized = forms.BooleanField(required=False)

    def __init__(self, project: Project, *args: Any, **kwargs: Any) -> None:
        """Initialize form with section choices from project."""
        super().__init__(*args, **kwargs)
        self.fields["section"] = forms.ModelChoiceField(
            queryset=project.section_set.all(),
            to_field_name="uuid",
            required=True,
        )


class TaskMoveForm(forms.Form):
    """Form for handling task move actions."""

    action = forms.CharField(required=True)
    direction = forms.ChoiceField(
        choices=[
            ("up", _("Up")),
            ("down", _("Down")),
        ]
    )

    def __init__(self, project: Project, *args: Any, **kwargs: Any) -> None:
        """Initialize form with task choices from project."""
        super().__init__(*args, **kwargs)
        # TODO rename to just 'task'
        self.fields["task_uuid"] = forms.ModelChoiceField(
            queryset=Task.objects.filter(section__project=project),
            to_field_name="uuid",
            required=True,
        )


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

    querydict = request.POST if request.method == "POST" else request.GET
    filter_by_team_member: Optional[QuerySet[TeamMember]] = None
    filter_by_label: Optional[QuerySet[Label]] = None
    filter_by_unlabeled: bool = False
    filter_by_unassigned: bool = False
    task_search_query: Optional[str] = None
    if len(querydict):
        labels = project.workspace.label_set.all()
        team_members = project.workspace.teammember_set.all()

        task_filter_form = ProjectFilterForm(
            team_members=team_members, labels=labels, data=querydict
        )
        if not task_filter_form.is_valid():
            raise BadRequest(task_filter_form.errors)

        filter_by_unassigned, filter_by_team_member = (
            task_filter_form.cleaned_data["filter_by_team_member"]
        )
        filter_by_unlabeled, filter_by_label = task_filter_form.cleaned_data[
            "filter_by_label"
        ]
        task_search_query = task_filter_form.cleaned_data["task_search_query"]

    qs = project_detail_query_set(
        filter_by_team_members=filter_by_team_member,
        unassigned_tasks=filter_by_unassigned,
        filter_by_labels=filter_by_label,
        unlabeled_tasks=filter_by_unlabeled,
        task_search_query=task_search_query,
        who=request.user,
        prefetch_labels=True,
    )

    context: dict[str, Any] = {}

    template = "workspace/project_detail.html"
    enrich_section: Optional[Section] = None
    match request.method, request.POST.get("action"):
        case "POST", "minimize_section":
            section_minimize_form = SectionMinimizeForm(
                project=project, data=request.POST
            )
            if not section_minimize_form.is_valid():
                raise BadRequest()

            enrich_section = section_minimize_form.cleaned_data["section"]
            minimized: bool = section_minimize_form.cleaned_data["minimized"]
            # TODO
            # setattr(enrich_section, "minimzed", minimized)

            section_minimize(
                who=request.user,
                section=section_minimize_form.cleaned_data["section"],
                minimized=minimized,
            )

            template = "workspace/project_detail/section.html"
        case "POST", "move_task":
            task_move_form = TaskMoveForm(project=project, data=request.POST)
            if not task_move_form.is_valid():
                raise BadRequest()
            task: Task = task_move_form.cleaned_data["task_uuid"]
            enrich_section = task.section
            task_move_in_direction(
                who=request.user,
                task=task,
                direction=task_move_form.cleaned_data["direction"],
            )
            template = "workspace/project_detail/section.html"
        case "POST", "minimize_team_member_filter":
            team_member_minimize_team_member_filter(
                team_member=team_member,
                minimized=request.POST.get("minimized") == "true",
            )
            template = "workspace/common/sidemenu/project_details.html"
        case "POST", "minimize_label_filter":
            team_member_minimize_label_filter(
                team_member=team_member,
                minimized=request.POST.get("minimized") == "true",
            )
            template = "workspace/common/sidemenu/project_details.html"
        case _:
            pass

    # TODO run this before the match: case:
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=qs
    )
    assert project, "Project disappeared"

    section: Optional[Section] = (
        next(
            filter(
                lambda s: s.pk == enrich_section.pk, project.section_set.all()
            ),
            None,
        )
        if enrich_section
        else None
    )
    context = {**context, "section": section}

    # Mark this project as most recently visited
    team_member_visit_project(team_member=team_member, project=project)

    project.workspace.quota = workspace_get_all_quotas(project.workspace)
    team_members = project.workspace.teammember_set.all()
    labels = project.workspace.label_set.all()

    task_filter_form = ProjectFilterForm(
        team_members=team_members,
        labels=labels,
        data=querydict,
    )

    context = {
        **context,
        **get_project_view_context(request, project.workspace),
        "project": project,
        "labels": labels,
        "team_members": team_members,
        "unassigned_tasks": filter_by_unassigned,
        "unlabeled_tasks": filter_by_unlabeled,
        "task_search_query": task_search_query,
        "task_filter_form": task_filter_form,
        "has_team_member_filter": filter_by_team_member is not None
        or filter_by_unassigned,
        "has_label_filter": filter_by_label is not None or filter_by_unlabeled,
    }
    return render(request, template, context)


class ProjectCreateForm(forms.Form):
    """Form for project creation."""

    title = forms.CharField(
        label=_("Project title"),
        widget=forms.TextInput(attrs={"placeholder": _("Project title")}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description for your project")}
        ),
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
            qs = workspace_build_detail_query_set(
                who=request.user, annotate_labels=True
            )
        case "POST":
            qs = None
        case other:
            # Should never be hit
            assert False, other
    workspace = workspace_find_by_workspace_uuid(
        workspace_uuid=workspace_uuid,
        who=request.user,
        qs=qs,
    )
    if workspace is None:
        raise Http404(_("No workspace found for this UUID"))

    if request.method == "GET":
        context = {
            **get_project_view_context(request, workspace),
            "form": ProjectCreateForm(),
        }
        return render(request, "workspace/project_create.html", context)

    form = ProjectCreateForm(request.POST)
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
            title=form.cleaned_data["title"],
            description=form.cleaned_data.get("description"),
            due_date=form.cleaned_data.get("due_date"),
            who=request.user,
            workspace=workspace,
        )
        return redirect("dashboard:projects:detail", project_uuid=project.uuid)
    except ValidationError as error:
        populate_form_with_drf_errors(form, error)
        context = {
            **get_project_view_context(request, workspace),
            "form": form,
        }
        return render(
            request, "workspace/project_create.html", context, status=400
        )


class ProjectUpdateForm(forms.Form):
    """Form for project updates."""

    title = forms.CharField(
        label=_("Project title"),
        widget=forms.TextInput(attrs={"placeholder": _("Project title")}),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description for your project")}
        ),
    )
    due_date = forms.DateField(
        required=False,
        label=_("Due date"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )


@require_http_methods(["GET", "POST"])
@platform_view
def project_update_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Update an existing project."""
    qs = project_detail_query_set(who=request.user, prefetch_labels=False)
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=qs
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))

    workspace = project.workspace

    context = {
        **get_project_view_context(request, workspace),
        "project": project,
    }

    if request.method == "GET":
        form = ProjectUpdateForm(
            initial={
                "title": project.title,
                "description": project.description,
            }
        )
        context = {"form": form, **context}
        return render(request, "workspace/project_update.html", context)

    form = ProjectUpdateForm(request.POST)
    if not form.is_valid():
        context = {"form": form, **context}
        return render(
            request, "workspace/project_update.html", context, status=400
        )

    try:
        project_update(
            who=request.user,
            project=project,
            title=form.cleaned_data["title"],
            description=form.cleaned_data.get("description"),
        )
        return redirect(
            "dashboard:workspaces:projects",
            workspace_uuid=project.workspace.uuid,
        )
    except ValidationError as error:
        populate_form_with_drf_errors(form, error)
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
        who=request.user,
        project_uuid=project_uuid,
        archived=False,
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
        who=request.user,
        project_uuid=project_uuid,
        archived=True,
    )
    if project is None:
        raise Http404(_("No archived project found for this uuid"))

    project_delete(project=project, who=request.user)
    return HttpResponseClientRefresh()
