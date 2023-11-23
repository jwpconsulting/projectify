"""Workspace board views."""
from uuid import UUID

from rest_framework import generics, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from workspace.models import Workspace, WorkspaceBoard, WorkspaceBoardQuerySet
from workspace.serializers.workspace_board import (
    WorkspaceBoardDetailSerializer,
)
from workspace.services.workspace_board import workspace_board_create


# TODO permission checking
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


class WorkspaceBoardRead(
    generics.RetrieveAPIView[
        WorkspaceBoard,
        WorkspaceBoardQuerySet,
        WorkspaceBoardDetailSerializer,
    ]
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
