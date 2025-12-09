# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Project views."""

from typing import Any
from uuid import UUID

from django import forms
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
from projectify.workspace.models import Project
from projectify.workspace.selectors.project import (
    ProjectDetailQuerySet,
    project_find_by_project_uuid,
    project_find_by_workspace_uuid,
)
from projectify.workspace.selectors.quota import workspace_get_all_quotas
from projectify.workspace.selectors.workspace import (
    workspace_find_by_workspace_uuid,
)
from projectify.workspace.serializers.base import ProjectBaseSerializer
from projectify.workspace.serializers.project import ProjectDetailSerializer
from projectify.workspace.services.project import (
    project_archive,
    project_create,
    project_delete,
    project_update,
)


# HTML
@platform_view
def project_detail_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Show project details."""
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=ProjectDetailQuerySet
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))
    project.workspace.quota = workspace_get_all_quotas(project.workspace)
    projects = project_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=project.workspace.uuid,
        archived=False,
    )
    context = {
        "project": project,
        "labels": list(project.workspace.label_set.values()),
        "projects": projects,
        "workspace": project.workspace,
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

    context: dict[str, Any] = {"workspace": workspace}

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
        context = {"form": form, **context}
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
        who=request.user,
        project_uuid=project_uuid,
        qs=Project.objects.select_related("workspace"),
    )
    if project is None:
        raise Http404(_("No project found for this uuid"))

    context: dict[str, Any] = {
        "project": project,
        "workspace": project.workspace,
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
