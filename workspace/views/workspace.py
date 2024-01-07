# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023, 2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Workspace CRUD views."""
import uuid
from typing import (
    Any,
)

from django.shortcuts import (
    get_object_or_404,
)

from rest_framework import (
    generics,
    parsers,
    views,
)
from rest_framework.request import (
    Request,
)
from rest_framework.response import (
    Response,
)

from workspace.selectors.workspace import WorkspaceDetailQuerySet
from workspace.services.workspace import (
    workspace_create,
    workspace_update,
)

from .. import (
    models,
)
from ..models.workspace import (
    Workspace,
    WorkspaceQuerySet,
)
from ..serializers.base import (
    WorkspaceBaseSerializer,
)
from ..serializers.workspace import (
    InviteUserToWorkspaceSerializer,
    WorkspaceDetailSerializer,
)


# Create
class WorkspaceCreate(
    generics.CreateAPIView[
        models.Workspace,
        models.WorkspaceQuerySet,
        WorkspaceBaseSerializer,
    ]
):
    """Create a workspace."""

    serializer_class = WorkspaceBaseSerializer

    def perform_create(self, serializer: WorkspaceBaseSerializer) -> None:
        """Create the workspace and add this user."""
        workspace = workspace_create(
            **serializer.validated_data, owner=self.request.user
        )
        # Kind of hacky, CreateAPIView relies on this being set when
        # serializing the result
        serializer.instance = workspace


# Read
class WorkspaceList(
    generics.ListAPIView[
        models.Workspace,
        models.WorkspaceQuerySet,
        WorkspaceBaseSerializer,
    ]
):
    """List all workspaces for a user."""

    queryset = models.Workspace.objects.all()
    serializer_class = WorkspaceBaseSerializer

    def get_queryset(self) -> models.WorkspaceQuerySet:
        """Filter by user."""
        user = self.request.user
        return self.queryset.get_for_user(user)


# Read + Update
class WorkspaceReadUpdate(
    generics.RetrieveUpdateAPIView[
        models.Workspace,
        models.WorkspaceQuerySet,
        WorkspaceDetailSerializer,
    ]
):
    """Workspace retrieve view."""

    serializer_class = WorkspaceDetailSerializer

    def get_object(self) -> models.Workspace:
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = WorkspaceDetailQuerySet
        qs = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_uuid"],
        )
        workspace: models.Workspace = get_object_or_404(qs)
        return workspace

    def perform_update(self, serializer: WorkspaceDetailSerializer) -> None:
        """Perform update."""
        instance = serializer.instance
        # This should not happen -- the point of updating is that we already
        # have an instance present
        if instance is None:
            raise ValueError("perform_update was called without instance")
        data = serializer.validated_data
        workspace_update(
            workspace=instance,
            title=data["title"],
            description=data.get("description"),
            who=self.request.user,
        )


# Delete


# RPC
class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(self, request: Request, uuid: uuid.UUID) -> Response:
        """Handle POST."""
        user = request.user
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            user,
            uuid,
        )
        workspace = get_object_or_404(qs)

        file_obj = request.data.get("file")
        if file_obj is None:
            workspace.picture.delete()
        else:
            workspace.picture = file_obj
        workspace.save()
        return Response(status=204)


class InviteUserToWorkspace(
    generics.CreateAPIView[
        Workspace, WorkspaceQuerySet, InviteUserToWorkspaceSerializer
    ]
):
    """Invite a user to a workspace."""

    lookup_field = "uuid"
    queryset = Workspace.objects.all()
    serializer_class = InviteUserToWorkspaceSerializer

    # A given TypedDict is a bit hard to override...
    def get_serializer_context(self) -> Any:
        """Enrich serializer context with workspace."""
        context = super().get_serializer_context()
        return {
            **context,
            "workspace": self.get_object(),
        }

    def get_queryset(self) -> WorkspaceQuerySet:
        """Search for workspace belonging to this user."""
        return models.Workspace.objects.filter_for_user_and_uuid(
            self.request.user,
            # We can look up by the uuid separately, I guess...
            # XXX this queryset will only have 0 or 1 results.
            self.kwargs["uuid"],
        )
