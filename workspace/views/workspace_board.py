"""Workspace board views."""
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import generics, serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from workspace.models import Workspace, WorkspaceBoard, WorkspaceBoardQuerySet
from workspace.selectors.workspace import workspace_find_by_workspace_uuid
from workspace.selectors.workspace_board import (
    WorkspaceBoardDetail,
    workspace_board_find_by_workspace_board_uuid,
    workspace_board_find_by_workspace_uuid,
)
from workspace.serializers.base import WorkspaceBoardBaseSerializer
from workspace.serializers.workspace_board import (
    WorkspaceBoardDetailSerializer,
)
from workspace.services.workspace_board import (
    workspace_board_archive,
    workspace_board_create,
    workspace_board_delete,
    workspace_board_update,
)


# Create
class WorkspaceBoardCreate(APIView):
    """Create a workspace board."""

    class InputSerializer(serializers.ModelSerializer[WorkspaceBoard]):
        """Parse workspace board creation input."""

        workspace_uuid = serializers.UUIDField()

        class Meta:
            """Restrict to the bare minimum needed for creation."""

            model = WorkspaceBoard
            fields = "title", "description", "workspace_uuid", "deadline"

    def post(self, request: Request) -> Response:
        """Create a workspace board."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace_uuid: UUID = serializer.validated_data.pop("workspace_uuid")
        workspace_qs = Workspace.objects.get_for_user(user).filter(
            uuid=workspace_uuid
        )
        # Workspace not found -> Raise 400, not 404
        workspace = get_object_or_404(workspace_qs)
        workspace_board = workspace_board_create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            deadline=serializer.validated_data.get("deadline"),
            who=user,
            workspace=workspace,
        )

        output_serializer = WorkspaceBoardDetailSerializer(
            instance=workspace_board
        )
        return Response(data=output_serializer.data, status=201)


# Read + Update + Delete
class WorkspaceBoardReadUpdateDelete(
    generics.UpdateAPIView[
        WorkspaceBoard,
        WorkspaceBoardQuerySet,
        WorkspaceBoardDetailSerializer,
    ],
    generics.DestroyAPIView[
        WorkspaceBoard,
        WorkspaceBoardQuerySet,
        WorkspaceBoardDetailSerializer,
    ],
):
    """Workspace board retrieve view."""

    queryset = WorkspaceBoard.objects.prefetch_related(
        "workspaceboardsection_set",
        "workspaceboardsection_set__task_set",
        "workspaceboardsection_set__task_set__assignee",
        "workspaceboardsection_set__task_set__assignee__user",
        "workspaceboardsection_set__task_set__labels",
        "workspaceboardsection_set__task_set__subtask_set",
    ).select_related(
        "workspace",
    )
    serializer_class = WorkspaceBoardDetailSerializer

    def get_object(self) -> WorkspaceBoard:
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset()
        qs = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_board_uuid"],
        )
        workspace_board: WorkspaceBoard = get_object_or_404(qs)
        return workspace_board

    def get(self, request: Request, workspace_board_uuid: UUID) -> Response:
        """Handle GET."""
        workspace_board = workspace_board_find_by_workspace_board_uuid(
            who=request.user,
            workspace_board_uuid=workspace_board_uuid,
            qs=WorkspaceBoardDetail,
        )
        if workspace_board is None:
            raise NotFound(_("No workspace board found for this uuid"))
        serializer = WorkspaceBoardDetailSerializer(
            instance=workspace_board,
        )
        return Response(serializer.data)

    def perform_update(
        self, serializer: WorkspaceBoardDetailSerializer
    ) -> None:
        """Update the workspace board."""
        if serializer.instance is None:
            # Unlikely to hit this, update can only be called with instance
            raise ValueError("Expected serializer instance")
        data = serializer.validated_data
        workspace_board_update(
            who=self.request.user,
            workspace_board=serializer.instance,
            title=data["title"],
            description=data.get("description"),
            deadline=data.get("deadline"),
        )

    def perform_destroy(self, instance: WorkspaceBoard) -> None:
        """Delete workspace board."""
        workspace_board_delete(
            who=self.request.user,
            workspace_board=instance,
        )


# List
class WorkspaceBoardArchivedList(APIView):
    """List archived workspace boards inside a workspace."""

    def get(self, request: Request, workspace_uuid: UUID) -> Response:
        """Get queryset."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid, who=request.user
        )
        if workspace is None:
            raise NotFound(_("No workspace found for this UUID"))
        workspace_boards = workspace_board_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            archived=True,
        )
        serializer = WorkspaceBoardBaseSerializer(
            instance=workspace_boards,
            many=True,
        )
        return Response(serializer.data)


# RPC
# TODO surely this can all be refactored
class WorkspaceBoardArchive(APIView):
    """Toggle the archived status of a board on or off."""

    class InputSerializer(serializers.Serializer):
        """Accept the desired archival status."""

        archived = serializers.BooleanField()

    def post(self, request: Request, workspace_board_uuid: UUID) -> Response:
        """Process request."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user
        workspace_board_qs = WorkspaceBoard.objects.filter_for_user_and_uuid(
            user=user,
            uuid=workspace_board_uuid,
        )
        workspace_board = get_object_or_404(workspace_board_qs)
        workspace_board_archive(
            workspace_board=workspace_board,
            archived=data["archived"],
            who=user,
        )
        workspace_board.refresh_from_db()
        output_serializer = WorkspaceBoardDetailSerializer(
            instance=workspace_board,
        )
        return Response(output_serializer.data, status=status.HTTP_200_OK)
