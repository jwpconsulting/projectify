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
"""Workspace serializers."""
from typing import (
    Any,
    Mapping,
    Optional,
)

from django.utils.translation import gettext_lazy as _

from rest_framework import (
    serializers,
)
from rest_framework.request import Request

from projectify.workspace.exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)
from projectify.workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
)

from ..models.workspace import (
    Workspace,
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
        request: Optional[Request] = self.context.get("request")
        if request is None:
            raise ValueError("context must contain request")
        user = request.user
        workspace: Workspace = self.context["workspace"]
        email: str = validated_data["email"]
        try:
            add_or_invite_workspace_user(
                who=user, workspace=workspace, email_or_user=email
            )
        except UserAlreadyInvited:
            raise serializers.ValidationError(
                {
                    "email": _(
                        "User with email {email} has already been invited to "
                        "this workspace."
                    ).format(email=email)
                }
            )
        except UserAlreadyAdded:
            raise serializers.ValidationError(
                {
                    "email": _(
                        "User with email {email} has already been added to "
                        "this workspace."
                    ).format(email=email)
                }
            )
        return validated_data
