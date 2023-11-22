"""Workspace views."""
from django.shortcuts import (
    get_object_or_404,
)

from rest_framework import (
    generics,
)

from .. import (
    models,
    serializers,
)


class WorkspaceBoardSectionRetrieve(
    generics.RetrieveAPIView[
        models.WorkspaceBoardSection,
        models.WorkspaceBoardSectionQuerySet,
        serializers.WorkspaceBoardSectionDetailSerializer,
    ]
):
    """Workspace board retrieve view."""

    queryset = models.WorkspaceBoardSection.objects.prefetch_related(
        "task_set",
        "task_set__assignee",
        "task_set__assignee__user",
        "task_set__labels",
        "task_set__subtask_set",
    ).select_related(
        "workspace_board",
        "workspace_board__workspace",
    )
    serializer_class = serializers.WorkspaceBoardSectionDetailSerializer

    def get_object(self) -> models.WorkspaceBoardSection:
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset()
        qs = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_board_section_uuid"],
        )
        workspace_board_section: models.WorkspaceBoardSection = (
            get_object_or_404(qs)
        )
        return workspace_board_section


class WorkspaceBoardArchivedList(
    generics.ListAPIView[
        models.WorkspaceBoard,
        models.WorkspaceBoardQuerySet,
        serializers.WorkspaceBoardBaseSerializer,
    ]
):
    """List archived workspace boards inside a workspace."""

    queryset = models.WorkspaceBoard.objects.filter_by_archived()
    serializer_class = serializers.WorkspaceBoardBaseSerializer

    def get_queryset(self) -> models.WorkspaceBoardQuerySet:
        """Get queryset."""
        user = self.request.user
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_uuid"],
        )
        workspace = get_object_or_404(qs)
        return self.queryset.filter_by_workspace(workspace)
