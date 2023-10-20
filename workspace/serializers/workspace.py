"""Workspace serializers."""
from typing import (
    Any,
    Mapping,
)

from django.utils.translation import gettext_lazy as _

from rest_framework import (
    serializers,
)

from workspace.exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)

from ..models.workspace import (
    Workspace,
)
from ..models.workspace_user_invite import (
    add_or_invite_workspace_user,
)
from . import (
    base,
)


class WorkspaceDetailSerializer(base.WorkspaceBaseSerializer):
    """
    Workspace detail serializer.

    Serializers ws board as well, but not the sections and so forth that they
    contain.
    """

    workspace_users = base.WorkspaceUserBaseSerializer(
        read_only=True, many=True, source="workspaceuser_set"
    )
    workspace_boards = base.WorkspaceBoardBaseSerializer(
        read_only=True, many=True, source="workspaceboard_set"
    )
    labels = base.LabelBaseSerializer(
        read_only=True, many=True, source="label_set"
    )

    class Meta(base.WorkspaceBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBaseSerializer.Meta.fields,
            "workspace_users",
            "workspace_boards",
            "labels",
        )


class InviteUserToWorkspaceSerializer(serializers.Serializer):
    """Serialize information needed to invite a user to a workspace."""

    email = serializers.EmailField()

    def create(self, validated_data: Mapping[str, Any]) -> Mapping[str, Any]:
        """Perform invitation."""
        workspace: Workspace = self.context["workspace"]
        email: str = validated_data["email"]
        try:
            add_or_invite_workspace_user(workspace, email)
        except UserAlreadyInvited:
            raise serializers.ValidationError(
                {"email": _("This user has already been invited")}
            )
        except UserAlreadyAdded:
            raise serializers.ValidationError(
                {"email": _("This user has already been added")}
            )
        return validated_data
