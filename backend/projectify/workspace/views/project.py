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

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.forms import populate_form_with_drf_errors
from projectify.lib.htmx import HttpResponseClientRefresh
from projectify.lib.schema import extend_schema
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view

from ..models import Project, Workspace
from ..models.label import Label
from ..models.team_member import TeamMember
from ..selectors.project import (
    ProjectDetailQuerySet,
    project_detail_query_set,
    project_find_by_project_uuid,
    project_find_by_workspace_uuid,
)
from ..selectors.quota import workspace_get_all_quotas
from ..selectors.team_member import team_member_find_for_workspace
from ..selectors.workspace import (
    workspace_build_detail_query_set,
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ..serializers.base import ProjectBaseSerializer
from ..serializers.project import ProjectDetailSerializer
from ..services.project import (
    project_archive,
    project_create,
    project_delete,
    project_update,
)
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
                label=_("Filter team members"),
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
            label=_("Filter labels"),
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


class MinimizeForm(forms.Form):
    """Form for handling minimize actions."""

    action = forms.CharField(required=True)
    minimized = forms.BooleanField(required=False)


# HTML
@require_http_methods(["GET", "POST"])
@platform_view
def project_detail_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Show project details."""
    if request.method == "POST":
        minimize_form = MinimizeForm(request.POST)
        if not minimize_form.is_valid():
            raise BadRequest()

        action = minimize_form.cleaned_data["action"]
        minimized = minimize_form.cleaned_data["minimized"]

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

        match action:
            case "minimize_team_member_filter":
                team_member_minimize_team_member_filter(
                    team_member=team_member,
                    minimized=minimized,
                )
            case "minimize_label_filter":
                team_member_minimize_label_filter(
                    team_member=team_member,
                    minimized=minimized,
                )
            case invalid:
                logger.warning("Invalid action %s", invalid)

        querydict = request.POST
    else:
        querydict = request.GET

    filter_by_team_member: Optional[QuerySet[TeamMember]] = None
    filter_by_label: Optional[QuerySet[Label]] = None
    filter_by_unlabeled: bool = False
    filter_by_unassigned: bool = False
    task_search_query: Optional[str] = None
    if len(querydict):
        logger.info("querydict %s", querydict)
        # We need to query the project an additional round here to
        # establish whether the labels and team members given to us
        # by the user are valid, or not
        project = project_find_by_project_uuid(
            who=request.user, project_uuid=project_uuid
        )
        if project is None:
            raise Http404(_("No project found for this uuid"))
        labels = project.workspace.label_set.all()
        team_members = project.workspace.teammember_set.all()

        task_filter_form = ProjectFilterForm(
            team_members=team_members, labels=labels, data=querydict
        )
        if not task_filter_form.is_valid():
            raise BadRequest(task_filter_form.errors)
        logger.info("filter form %s", task_filter_form.cleaned_data)

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
    )
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=qs
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))

    # Mark this project as most recently visited
    team_member_qs = getattr(project.workspace, "current_team_member_qs", None)
    assert team_member_qs
    team_member_visit_project(team_member=team_member_qs[0], project=project)

    project.workspace.quota = workspace_get_all_quotas(project.workspace)
    team_members = project.workspace.teammember_set.all()
    labels = project.workspace.label_set.all()

    task_filter_form = ProjectFilterForm(
        team_members=team_members,
        labels=labels,
        data=querydict,
    )

    context = {
        **get_project_view_context(request, project.workspace),
        "project": project,
        "labels": labels,
        "team_members": team_members,
        "unassigned_tasks": filter_by_unassigned,
        "unlabeled_tasks": filter_by_unlabeled,
        "task_search_query": task_search_query,
        "task_filter_form": task_filter_form,
    }
    return render(request, "workspace/project_detail.html", context)


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


# Create
class ProjectCreate(APIView):
    """Create a project."""

    class ProjectCreateSerializer(serializers.ModelSerializer[Project]):
        """Parse project creation input."""

        workspace_uuid = serializers.UUIDField()

        class Meta:
            """Restrict to the bare minimum needed for creation."""

            model = Project
            fields = "title", "description", "workspace_uuid", "due_date"

    @extend_schema(
        request=ProjectCreateSerializer,
        responses={201: ProjectDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Create a project."""
        user = request.user
        serializer = self.ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace_uuid: UUID = serializer.validated_data.pop("workspace_uuid")
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid,
            who=user,
        )
        if workspace is None:
            raise serializers.ValidationError(
                {"workspace_uuid": _("No workspace found for this UUID")}
            )
        project = project_create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            due_date=serializer.validated_data.get("due_date"),
            who=user,
            workspace=workspace,
        )

        output_serializer = ProjectBaseSerializer(instance=project)
        return Response(data=output_serializer.data, status=201)


# Read + Update + Delete
class ProjectReadUpdateDelete(APIView):
    """Project retrieve view."""

    @extend_schema(
        responses={200: ProjectDetailSerializer},
    )
    def get(self, request: Request, project_uuid: UUID) -> Response:
        """Handle GET."""
        project = project_find_by_project_uuid(
            who=request.user,
            project_uuid=project_uuid,
            qs=ProjectDetailQuerySet,
        )
        if project is None:
            raise NotFound(_("No project found for this uuid"))
        project.workspace.quota = workspace_get_all_quotas(project.workspace)
        serializer = ProjectDetailSerializer(instance=project)
        return Response(serializer.data)

    class ProjectUpdateSerializer(serializers.ModelSerializer[Project]):
        """Serializer for PUT."""

        class Meta:
            """Meta."""

            model = Project
            fields = (
                "title",
                "description",
                "due_date",
            )

    @extend_schema(
        request=ProjectUpdateSerializer,
        responses={200: ProjectUpdateSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request, project_uuid: UUID) -> Response:
        """Handle PUT."""
        project = project_find_by_project_uuid(
            who=request.user,
            project_uuid=project_uuid,
        )
        if project is None:
            raise NotFound(_("No project found for this uuid"))
        serializer = self.ProjectUpdateSerializer(
            instance=project,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        project_update(
            who=self.request.user,
            project=project,
            title=data["title"],
            description=data.get("description"),
            due_date=data.get("due_date"),
        )
        return Response(data, status.HTTP_200_OK)

    @extend_schema(
        responses={204: None},
    )
    def delete(self, request: Request, project_uuid: UUID) -> Response:
        """Handle DELETE."""
        project = project_find_by_project_uuid(
            who=request.user,
            project_uuid=project_uuid,
            archived=True,
        )
        if project is None:
            raise NotFound(_("No project found for this uuid"))
        project_delete(
            who=self.request.user,
            project=project,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


# List
class ProjectArchivedList(APIView):
    """List archived projects inside a workspace."""

    class ArchivedProjectSerializer(serializers.ModelSerializer[Project]):
        """Serialize an archived project."""

        class Meta:
            """Include only the bare minimum."""

            model = Project
            fields = (
                "title",
                "uuid",
                "archived",
            )

    @extend_schema(
        request=None,
        responses={200: ArchivedProjectSerializer(many=True)},
    )
    def get(self, request: Request, workspace_uuid: UUID) -> Response:
        """Get queryset."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid, who=request.user
        )
        if workspace is None:
            raise NotFound(_("No workspace found for this UUID"))
        projects = project_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            archived=True,
        )
        serializer = self.ArchivedProjectSerializer(
            instance=projects,
            many=True,
        )
        return Response(serializer.data)


# RPC
# TODO surely this can all be refactored
class ProjectArchive(APIView):
    """Toggle the archived status of a board on or off."""

    class ProjectArchiveSerializer(serializers.Serializer):
        """Accept the desired archival status."""

        archived = serializers.BooleanField()

    @extend_schema(
        request=ProjectArchiveSerializer,
        responses={204: None, 400: DeriveSchema},
    )
    def post(self, request: Request, project_uuid: UUID) -> Response:
        """Process request."""
        serializer = self.ProjectArchiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        archived = serializer.validated_data["archived"]
        project = project_find_by_project_uuid(
            project_uuid=project_uuid,
            who=request.user,
            archived=not archived,
        )
        if project is None:
            raise NotFound(
                _("No project found for this UUID where archived={}").format(
                    not archived
                )
            )
        project_archive(project=project, archived=archived, who=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
