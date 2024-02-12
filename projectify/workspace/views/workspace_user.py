# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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

from rest_framework import (
    generics,
)

from workspace.serializers.base import (
    WorkspaceUserBaseSerializer,
)
from workspace.services.workspace_user import (
    workspace_user_delete,
    workspace_user_update,
)

from ..models.workspace_user import (
    WorkspaceUser,
    WorkspaceUserQuerySet,
)


# Create
# TODO make me an APIView
# Read + Update + Delete
class WorkspaceUserReadUpdateDelete(
    generics.RetrieveUpdateDestroyAPIView[
        WorkspaceUser, WorkspaceUserQuerySet, WorkspaceUserBaseSerializer
    ]
):
    """Delete a workspace user."""

    serializer_class = WorkspaceUserBaseSerializer
    queryset = WorkspaceUser.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "workspace_user_uuid"

    def get_queryset(self) -> WorkspaceUserQuerySet:
        """Restrict to this user's workspace's workspace users."""
        return self.queryset.filter_by_user(self.request.user)

    # TODO replace with normal def put(
    def perform_update(self, serializer: WorkspaceUserBaseSerializer) -> None:
        """Update the workspace user."""
        instance = serializer.instance
        if instance is None:
            raise ValueError("Expected workspace user instance")
        data = serializer.validated_data
        workspace_user_update(
            workspace_user=instance,
            who=self.request.user,
            role=data["role"],
            job_title=data.get("job_title"),
        )

    # TODO replace with normal def delete(
    def perform_destroy(self, instance: WorkspaceUser) -> None:
        """Perform destroy."""
        workspace_user_delete(who=self.request.user, workspace_user=instance)
