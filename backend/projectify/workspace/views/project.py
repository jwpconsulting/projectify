# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Project views."""

from typing import Optional, cast
from uuid import UUID

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.schema import extend_schema
from projectify.user.models.user import User
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
class ProjectDetailView(DetailView):
    """Show project details."""

    pk_url_kwar = "project_uuid"

    def get_object(
        self, queryset: Optional[QuerySet[Project]] = None
    ) -> Project:
        """Get the right project for the current user."""
        project_uuid = self.kwargs["project_uuid"]
        project = project_find_by_project_uuid(
            who=cast(User, self.request.user),
            project_uuid=project_uuid,
            qs=queryset or ProjectDetailQuerySet,
        )
        if project is None:
            raise NotFound(_("No project found for this uuid"))
        project.workspace.quota = workspace_get_all_quotas(project.workspace)
        return project


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
