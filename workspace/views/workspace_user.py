"""Views for workspace user."""
from django.utils.translation import gettext_lazy as _

from rest_framework import (
    generics,
    serializers,
)

from workspace.serializers.base import (
    WorkspaceUserBaseSerializer,
)
from workspace.services.workspace_user import workspace_user_update

from ..models.workspace_user import (
    WorkspaceUser,
    WorkspaceUserQuerySet,
)

# Create
# Read
# Update
# Delete


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

    # TODO refactor into service layer
    def perform_destroy(self, instance: WorkspaceUser) -> None:
        """
        Validate that own user can not be deleted.

        We do not support deleting one's own workspace user for now. This is
        to avoid that if a user is an admin, that they will leave the workspace
        inoperable.

        On the other hand, we might introduce a proper hand-off procedure,
        so big TODO maybe?
        """
        if instance.user == self.request.user:
            raise serializers.ValidationError(
                {"workspace_user": _("Can't delete own workspace user")}
            )
        super().perform_destroy(instance)
