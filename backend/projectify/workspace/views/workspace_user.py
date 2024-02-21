# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Views for workspace user."""
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import (
    serializers,
    views,
)
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from projectify.workspace.selectors.workspace_user import (
    workspace_user_find_by_workspace_user_uuid,
)
from projectify.workspace.serializers.base import (
    WorkspaceUserBaseSerializer,
)
from projectify.workspace.services.workspace_user import (
    workspace_user_delete,
    workspace_user_update,
)

from ..models.workspace_user import (
    WorkspaceUser,
    WorkspaceUserQuerySet,
)


# Create
# Read + Update + Delete
class WorkspaceUserReadUpdateDelete(views.APIView):
    """Delete a workspace user."""

    serializer_class = WorkspaceUserBaseSerializer
    queryset = WorkspaceUser.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "workspace_user_uuid"

    def get_queryset(self) -> WorkspaceUserQuerySet:
        """Restrict to this user's workspace's workspace users."""
        return self.queryset.filter_by_user(self.request.user)

    def get(self, request: Request, workspace_user_uuid: UUID) -> Response:
        """Handle GET."""
        workspace_user = workspace_user_find_by_workspace_user_uuid(
            who=request.user,
            workspace_user_uuid=workspace_user_uuid,
        )
        if workspace_user is None:
            raise NotFound(_("Could not find workspace user for given UUID"))

        serializer = WorkspaceUserBaseSerializer(
            instance=workspace_user,
        )

        return Response(status=HTTP_200_OK, data=serializer.data)

    class InputSerializer(serializers.ModelSerializer[WorkspaceUser]):
        """Serializer for PUT updates."""

        class Meta:
            """Accept job_title, role."""

            fields = "job_title", "role"
            model = WorkspaceUser

    def put(self, request: Request, workspace_user_uuid: UUID) -> Response:
        """Handle PUT."""
        workspace_user = workspace_user_find_by_workspace_user_uuid(
            who=request.user,
            workspace_user_uuid=workspace_user_uuid,
        )
        if workspace_user is None:
            raise NotFound(_("Could not find workspace user for given UUID"))

        serializer = self.InputSerializer(
            data=request.data,
            instance=workspace_user,
        )
        serializer.is_valid(raise_exception=True)
        workspace_user_update(
            workspace_user=workspace_user,
            who=request.user,
            role=serializer.validated_data["role"],
            job_title=serializer.validated_data.get("job_title"),
        )
        return Response(status=HTTP_200_OK, data=serializer.data)

    def delete(self, request: Request, workspace_user_uuid: UUID) -> Response:
        """Handle DELETE."""
        workspace_user = workspace_user_find_by_workspace_user_uuid(
            who=request.user,
            workspace_user_uuid=workspace_user_uuid,
        )
        if workspace_user is None:
            raise NotFound(_("Could not find workspace user for given UUID"))
        workspace_user_delete(
            who=self.request.user, workspace_user=workspace_user
        )
        return Response(status=HTTP_204_NO_CONTENT)
