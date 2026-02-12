# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Project views."""

import logging
from typing import Any, Optional
from uuid import UUID

from django import forms
from django.core.exceptions import BadRequest
from django.db.models import QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

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

from ..models import Project
from ..models.label import Label
from ..models.team_member import TeamMember
from ..selectors.project import (
    ProjectDetailQuerySet,
    project_detail_query_set,
    project_find_by_project_uuid,
    project_find_by_workspace_uuid,
)
from ..selectors.quota import workspace_get_all_quotas
from ..selectors.workspace import (
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
from ..services.team_member import team_member_visit_project

logger = logging.getLogger(__name__)


class ProjectFilterForm(forms.Form):
    """Form for deserializing project task filters."""

    filter_by_unassigned = forms.BooleanField(
        label=_("Assigned to nobody"), required=False
    )
    filter_by_unlabeled = forms.BooleanField(
        label=_("No label"), required=False
    )
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
        member_widget = forms.CheckboxSelectMultiple()
        member_widget.option_template_name = (
            "workspace/forms/widgets/select_team_member_option.html"
        )
        self.fields["filter_by_team_member"] = forms.ModelMultipleChoiceField(
            required=False,
            blank=True,
            label=_("Filter team members"),
            queryset=team_members,
            widget=member_widget,
            to_field_name="uuid",
        )
        label_widget = forms.CheckboxSelectMultiple()
        label_widget.option_template_name = (
            "workspace/forms/widgets/select_label_option.html"
        )
        self.fields["filter_by_label"] = forms.ModelMultipleChoiceField(
            required=False,
            label=_("Filter labels"),
            queryset=labels,
            widget=label_widget,
            to_field_name="uuid",
        )

    def clean(self) -> dict[str, Any]:
        """Override clean and make empty fields None instead."""
        data = super().clean()
        if not data["filter_by_team_member"].exists():
            data["filter_by_team_member"] = None
        if not data["filter_by_label"].exists():
            data["filter_by_label"] = None
        if data["task_search_query"] == "":
            data["task_search_query"] = None
        return data


# HTML
@platform_view
def project_detail_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Show project details."""
    filter_by_team_member: Optional[QuerySet[TeamMember]] = None
    filter_by_label: Optional[QuerySet[Label]] = None
    filter_by_unlabeled: bool = False
    filter_by_unassigned: bool = False
    task_search_query: Optional[str] = None
    match len(request.GET):
        case 0:
            pass
        case _:
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
                team_members=team_members, labels=labels, data=request.GET
            )
            if not task_filter_form.is_valid():
                raise BadRequest(task_filter_form.errors)

            filter_by_team_member = task_filter_form.cleaned_data[
                "filter_by_team_member"
            ]
            filter_by_unassigned = task_filter_form.cleaned_data[
                "filter_by_unassigned"
            ]
            filter_by_label = task_filter_form.cleaned_data["filter_by_label"]
            filter_by_unlabeled = task_filter_form.cleaned_data[
                "filter_by_unlabeled"
            ]
            task_search_query = task_filter_form.cleaned_data[
                "task_search_query"
            ]

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
    team_member_visit_project(user=request.user, project=project)

    project.workspace.quota = workspace_get_all_quotas(project.workspace)
    projects = project.workspace.project_set.all()
    team_members = project.workspace.teammember_set.all()
    labels = project.workspace.label_set.all()

    task_filter_form = ProjectFilterForm(
        team_members=team_members,
        labels=labels,
        data=request.GET,
    )

    context = {
        "project": project,
        "labels": labels,
        "projects": projects,
        "workspaces": workspace_find_for_user(who=request.user),
        "workspace": project.workspace,
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


@platform_view
def project_create_view(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Create a new project in a workspace."""
    workspace = workspace_find_by_workspace_uuid(
        workspace_uuid=workspace_uuid,
        who=request.user,
    )
    if workspace is None:
        raise Http404(_("No workspace found for this UUID"))

    # XXX inefficient
    projects = project_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace.uuid,
        archived=False,
    )

    context: dict[str, Any] = {
        "workspace": workspace,
        "projects": projects,
        "workspaces": workspace_find_for_user(who=request.user),
    }

    if request.method == "GET":
        form = ProjectCreateForm()
        context = {"form": form, **context}
        return render(request, "workspace/project_create.html", context)

    form = ProjectCreateForm(request.POST)
    if not form.is_valid():
        context = {"form": form, **context}
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
        context = {**context, "form": form}
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


@platform_view
def project_update_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Update an existing project."""
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=ProjectDetailQuerySet
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))

    workspace = project.workspace

    context: dict[str, Any] = {
        "project": project,
        "workspace": workspace,
        "projects": project.workspace.project_set.all(),
        "workspaces": workspace_find_for_user(who=request.user),
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


@platform_view
def project_archive_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Archive a project via HTMX."""
    if request.method != "POST":
        return HttpResponse(status=405)
    project = project_find_by_project_uuid(
        who=request.user,
        project_uuid=project_uuid,
        archived=False,
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))
    project_archive(project=project, archived=True, who=request.user)
    return HttpResponseClientRefresh()


@platform_view
def project_recover_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Recover an archived project via HTMX."""
    if request.method != "POST":
        return HttpResponse(status=405)

    project = project_find_by_project_uuid(
        who=request.user,
        project_uuid=project_uuid,
        archived=True,
    )
    if project is None:
        raise Http404(_("No archived project found for this uuid"))

    project_archive(project=project, archived=False, who=request.user)
    return HttpResponseClientRefresh()


@platform_view
def project_delete_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Delete an archived project via HTMX."""
    if request.method != "POST":
        return HttpResponse(status=405)

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
