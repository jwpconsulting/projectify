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

from django.shortcuts import (
    get_object_or_404,
)
from django.utils.translation import gettext_lazy as _

from rest_framework import (
    generics,
    parsers,
    serializers,
    views,
)
from rest_framework.exceptions import NotFound
from rest_framework.request import (
    Request,
)
from rest_framework.response import (
    Response,
)
from rest_framework.status import HTTP_201_CREATED

from projectify.workspace.exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)
from projectify.workspace.selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_find_by_workspace_uuid,
)
from projectify.workspace.services.workspace import (
    workspace_create,
    workspace_update,
)
from projectify.workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
)

from .. import (
    models,
)
from ..models.workspace import (
    WorkspaceQuerySet,
)
from ..serializers.base import (
    WorkspaceBaseSerializer,
)
from ..serializers.workspace import (
    WorkspaceDetailSerializer,
)


# Create
class WorkspaceCreate(
    generics.CreateAPIView[
        models.Workspace,
        WorkspaceQuerySet,
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
        WorkspaceQuerySet,
        WorkspaceBaseSerializer,
    ]
):
    """List all workspaces for a user."""

    queryset = models.Workspace.objects.all()
    serializer_class = WorkspaceBaseSerializer

    def get_queryset(self) -> WorkspaceQuerySet:
        """Filter by user."""
        user = self.request.user
        return self.queryset.get_for_user(user)


# TODO use regular APIView
# Read + Update
class WorkspaceReadUpdate(
    generics.RetrieveUpdateAPIView[
        models.Workspace,
        WorkspaceQuerySet,
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


class InviteUserToWorkspace(views.APIView):
    """Invite a user to a workspace."""

    class InputSerializer(serializers.Serializer):
        """Accept email."""

        email = serializers.EmailField()

    def post(self, request: Request, uuid: uuid.UUID) -> Response:
        """Handle POST."""
        user = request.user
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=uuid,
            who=user,
        )
        if workspace is None:
            raise NotFound(_("No workspace found for this UUID"))

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data["email"]
        try:
            add_or_invite_workspace_user(
                who=user, workspace=workspace, email_or_user=email
            )
        except UserAlreadyInvited:
            raise serializers.ValidationError(
                {
                    "email": _(
                        "User with email {email} has already been invited to "
                        "this workspace."
                    ).format(email=email)
                }
            )
        except UserAlreadyAdded:
            raise serializers.ValidationError(
                {
                    "email": _(
                        "User with email {email} has already been added to "
                        "this workspace."
                    ).format(email=email)
                }
            )
        return Response(status=HTTP_201_CREATED)
