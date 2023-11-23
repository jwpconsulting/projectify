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
