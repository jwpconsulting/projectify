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
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import (
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
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from projectify.workspace.selectors.quota import workspace_get_all_quotas

from ..exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)
from ..models import Workspace
from ..selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ..serializers.base import (
    WorkspaceBaseSerializer,
)
from ..serializers.workspace import (
    WorkspaceDetailSerializer,
)
from ..services.workspace import (
    workspace_create,
    workspace_update,
)
from ..services.workspace_user_invite import (
    workspace_user_invite_create,
)


# Create
class WorkspaceCreate(views.APIView):
    """Create a workspace."""

    class InputSerializer(serializers.ModelSerializer[Workspace]):
        """Accept title, description."""

        class Meta:
            """Meta."""

            fields = "title", "description"
            model = Workspace

    def post(self, request: Request) -> Response:
        """Create the workspace and add this user."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace = workspace_create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            owner=self.request.user,
        )
        result = WorkspaceBaseSerializer(instance=workspace)
        return Response(status=HTTP_201_CREATED, data=result.data)


# Read
class WorkspaceList(views.APIView):
    """List all workspaces for a user."""

    def get(self, request: Request) -> Response:
        """Handle GET."""
        workspaces = workspace_find_for_user(who=request.user)
        serializer = WorkspaceBaseSerializer(instance=workspaces, many=True)
        return Response(status=HTTP_200_OK, data=serializer.data)


# Read + Update
class WorkspaceReadUpdate(views.APIView):
    """Workspace read and update view."""

    def get(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle GET."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            qs=WorkspaceDetailQuerySet,
        )
        if workspace is None:
            raise NotFound(_("Could not find workspace with this UUID"))
        workspace.quota = workspace_get_all_quotas(workspace)
        serializer = WorkspaceDetailSerializer(instance=workspace)
        return Response(status=HTTP_200_OK, data=serializer.data)

    class InputSerializer(serializers.ModelSerializer[Workspace]):
        """Accept title, description."""

        class Meta:
            """Meta."""

            fields = "title", "description"
            model = Workspace

    def put(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle PUT."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            qs=WorkspaceDetailQuerySet,
        )
        if workspace is None:
            raise NotFound(_("Could not find workspace with this UUID"))

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace_update(
            workspace=workspace,
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            who=self.request.user,
        )
        return Response(status=HTTP_200_OK, data=serializer.data)


# Delete


# RPC
class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(self, request: Request, uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=uuid,
        )
        if workspace is None:
            raise NotFound(
                _("Could not find workspace with UUID for picture upload")
            )

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

    def post(self, request: Request, uuid: UUID) -> Response:
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
            workspace_user_invite_create(
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
        return Response(data=serializer.data, status=HTTP_201_CREATED)
