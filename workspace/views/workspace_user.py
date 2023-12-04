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
