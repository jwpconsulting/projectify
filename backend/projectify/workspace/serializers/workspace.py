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
from rest_framework import serializers

from . import base


class WorkspaceUserInviteSerializer(serializers.Serializer):
    """Serializer workspace user invites."""

    email = serializers.EmailField(source="user_invite.email")
    created = serializers.DateTimeField()


class SingleQuotaSerializer(serializers.Serializer):
    """Serializer a single Quota dataclass."""

    current = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)
    can_create_more = serializers.BooleanField()


class WorkspaceQuotaSerializer(serializers.Serializer):
    """Serializer quota."""

    # full | trial | inactive
    workspace_status = serializers.CharField()
    chat_messages = SingleQuotaSerializer()
    labels = SingleQuotaSerializer()
    sub_tasks = SingleQuotaSerializer()
    tasks = SingleQuotaSerializer()
    task_labels = SingleQuotaSerializer()
    workspace_boards = SingleQuotaSerializer()
    workspace_board_sections = SingleQuotaSerializer()
    workspace_users_and_invites = SingleQuotaSerializer()


class WorkspaceDetailSerializer(base.WorkspaceBaseSerializer):
    """
    Workspace detail serializer.

    Serializers ws board as well, but not the sections and so forth that they
    contain.
    """

    workspace_users = base.WorkspaceUserBaseSerializer(
        read_only=True, many=True, source="workspaceuser_set"
    )
    workspace_user_invites = WorkspaceUserInviteSerializer(
        read_only=True, many=True, source="workspaceuserinvite_set"
    )
    workspace_boards = base.WorkspaceBoardBaseSerializer(
        read_only=True, many=True, source="workspaceboard_set"
    )
    labels = base.LabelBaseSerializer(
        read_only=True, many=True, source="label_set"
    )
    quota = WorkspaceQuotaSerializer()

    class Meta(base.WorkspaceBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBaseSerializer.Meta.fields,
            "workspace_users",
            "workspace_user_invites",
            "workspace_boards",
            "labels",
            "quota",
        )
