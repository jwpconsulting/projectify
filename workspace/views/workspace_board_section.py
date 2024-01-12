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
"""Workspace board section views."""
from uuid import UUID

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from workspace.models import (
    WorkspaceBoard,
    WorkspaceBoardSection,
)
from workspace.models.workspace_board_section import (
    WorkspaceBoardSectionQuerySet,
)
from workspace.selectors.workspace_board_section import (
    find_workspace_board_section_for_user_and_uuid,
)
from workspace.serializers.workspace_board_section import (
    WorkspaceBoardSectionDetailSerializer,
)
from workspace.services.workspace_board_section import (
    workspace_board_section_create,
    workspace_board_section_delete,
    workspace_board_section_move,
    workspace_board_section_update,
)


class WorkspaceBoardSectionCreate(APIView):
    """Create a workspace board section."""

    class InputSerializer(serializers.ModelSerializer[WorkspaceBoardSection]):
        """Parse workspace board section creation input."""

        workspace_board_uuid = serializers.UUIDField()

        class Meta:
            """Restrict fields to bare minimum needed for section creation."""

            model = WorkspaceBoardSection
            fields = "title", "description", "workspace_board_uuid"

    def post(self, request: Request) -> Response:
        """Create a workspace board section."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        workspace_board_uuid: UUID = data["workspace_board_uuid"]
        workspace_board_qs = WorkspaceBoard.objects.filter_for_user_and_uuid(
            user=user,
            uuid=workspace_board_uuid,
        )
        try:
            workspace_board = workspace_board_qs.get()
        except WorkspaceBoard.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "workspace_board_uuid": _(
                        "Could not find a workspace board with this uuid"
                    )
                }
            )
        workspace_board_section = workspace_board_section_create(
            workspace_board=workspace_board,
            title=data["title"],
            description=data.get("description"),
            who=user,
        )
        output_serializer = WorkspaceBoardSectionDetailSerializer(
            instance=workspace_board_section,
        )
        return Response(data=output_serializer.data, status=201)


# Read + Update + Delete
class WorkspaceBoardSectionReadUpdateDelete(
    generics.RetrieveUpdateAPIView[
        WorkspaceBoardSection,
        WorkspaceBoardSectionQuerySet,
        WorkspaceBoardSectionDetailSerializer,
    ]
):
    """Workspace board retrieve view."""

    # TODO make me
    # workspace/selectors/workspace_board_section.py:WorkspaceBoardSectionDetail
    queryset = WorkspaceBoardSection.objects.prefetch_related(
        "task_set",
        "task_set__assignee",
        "task_set__assignee__user",
        "task_set__labels",
        "task_set__subtask_set",
    ).select_related(
        "workspace_board",
        "workspace_board__workspace",
    )
    serializer_class = WorkspaceBoardSectionDetailSerializer

    def get_object(self) -> WorkspaceBoardSection:
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset()
        qs = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_board_section_uuid"],
        )
        workspace_board_section: WorkspaceBoardSection = get_object_or_404(qs)
        return workspace_board_section

    def perform_update(
        self, serializer: WorkspaceBoardSectionDetailSerializer
    ) -> None:
        """Update workspace board section."""
        if serializer.instance is None:
            raise ValueError("Expected serializer.instance")
        data = serializer.validated_data
        workspace_board_section_update(
            who=self.request.user,
            workspace_board_section=serializer.instance,
            title=data["title"],
            description=data.get("description"),
        )

    def delete(
        self, request: Request, workspace_board_section_uuid: UUID
    ) -> Response:
        """Handle DELETE."""
        workspace_board_section = (
            find_workspace_board_section_for_user_and_uuid(
                user=request.user,
                workspace_board_section_uuid=workspace_board_section_uuid,
            )
        )
        if workspace_board_section is None:
            raise NotFound(
                _("Workspace board section not found for this UUID")
            )
        workspace_board_section_delete(
            who=self.request.user,
            workspace_board_section=workspace_board_section,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


# RPC
class WorkspaceBoardSectionMove(APIView):
    """Insert a workspace board section at a given position."""

    class InputSerializer(serializers.Serializer):
        """Accept the desired position within workspace board."""

        order = serializers.IntegerField()

    def post(
        self, request: Request, workspace_board_section_uuid: UUID
    ) -> Response:
        """Process request."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user
        workspace_board_section_qs = (
            WorkspaceBoardSection.objects.filter_for_user_and_uuid(
                user=user,
                uuid=workspace_board_section_uuid,
            )
        )
        workspace_board_section = get_object_or_404(workspace_board_section_qs)
        workspace_board_section_move(
            workspace_board_section=workspace_board_section,
            order=data["order"],
            who=user,
        )
        workspace_board_section.refresh_from_db()
        return Response(status=status.HTTP_200_OK)
