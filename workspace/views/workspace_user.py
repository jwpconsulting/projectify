"""Views for workspace user."""
from django.utils.translation import gettext_lazy as _

# Create
# Read
# Update
# Delete
from rest_framework import (
    generics,
    serializers,
)

from workspace.serializers.base import (
    WorkspaceUserBaseSerializer,
)

from ..models.workspace_user import (
    WorkspaceUser,
    WorkspaceUserQuerySet,
)


class WorkspaceUserDestroy(
    generics.DestroyAPIView[
        WorkspaceUser, WorkspaceUserQuerySet, WorkspaceUserBaseSerializer
    ]
):
    """Delete a workspace user."""

    queryset = WorkspaceUser.objects.all()
    lookup_field = "uuid"

    def get_queryset(self) -> WorkspaceUserQuerySet:
        """Restrict to this user's workspace's workspace users."""
        return self.queryset.filter_by_user(self.request.user)

    def get_object(self) -> WorkspaceUser:
        """
        Retrieve workspace user.

        We do not support deleting one's own workspace user for now. This is
        to avoid that if a user is an admin, that they will leave the workspace
        inoperable.

        On the other hand, we might introduce a proper hand-off procedure,
        so big TODO maybe?
        """
        result = super().get_object()
        if result.user == self.request.user:
            raise serializers.ValidationError(
                {"workspace_user": _("Can't delete own workspace user")}
            )
        return result
