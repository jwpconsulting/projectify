"""Workspace board section views."""
from uuid import UUID

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.utils import validate_perm
from workspace.models import (
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceBoardSectionQuerySet,
)
from workspace.serializers.workspace_board_section import (
    WorkspaceBoardSectionDetailSerializer,
)
from workspace.services.workspace_board_section import (
    workspace_board_section_create,
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


# Read
class WorkspaceBoardSectionRead(
    generics.RetrieveAPIView[
        WorkspaceBoardSection,
        WorkspaceBoardSectionQuerySet,
        WorkspaceBoardSectionDetailSerializer,
    ]
):
    """Workspace board retrieve view."""

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
        validate_perm(
            "workspace.can_update_workspace_board_section",
            user,
            workspace_board_section,
        )
        workspace_board_section.move_to(data["order"])
        workspace_board_section.refresh_from_db()
        output_serializer = WorkspaceBoardSectionDetailSerializer(
            instance=workspace_board_section,
        )
        return Response(output_serializer.data, status=status.HTTP_200_OK)
