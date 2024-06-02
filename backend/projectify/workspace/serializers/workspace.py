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


class TeamMemberInviteSerializer(serializers.Serializer):
    """Serializer team member invites."""

    email = serializers.EmailField(source="user_invite.email")
    created = serializers.DateTimeField()


class SingleQuotaSerializer(serializers.Serializer):
    """Serializer a single Quota dataclass."""

    current = serializers.IntegerField(allow_null=True)
    limit = serializers.IntegerField(allow_null=True)
    can_create_more = serializers.BooleanField()


class WorkspaceQuotaSerializer(serializers.Serializer):
    """Serializer quota."""

    # full | trial | inactive
    workspace_status = serializers.ChoiceField(
        choices=["full", "trial", "inactive"]
    )
    chat_messages = SingleQuotaSerializer()
    labels = SingleQuotaSerializer()
    sub_tasks = SingleQuotaSerializer()
    tasks = SingleQuotaSerializer()
    task_labels = SingleQuotaSerializer()
    projects = SingleQuotaSerializer()
    sections = SingleQuotaSerializer()
    team_members_and_invites = SingleQuotaSerializer()


class WorkspaceDetailSerializer(base.WorkspaceBaseSerializer):
    """
    Workspace detail serializer.

    Serializers ws board as well, but not the sections and so forth that they
    contain.
    """

    team_members = base.TeamMemberBaseSerializer(
        read_only=True, many=True, source="teammember_set"
    )
    team_member_invites = TeamMemberInviteSerializer(
        read_only=True, many=True, source="teammemberinvite_set"
    )
    projects = base.ProjectBaseSerializer(
        read_only=True, many=True, source="project_set"
    )
    labels = base.LabelBaseSerializer(
        read_only=True, many=True, source="label_set"
    )
    quota = WorkspaceQuotaSerializer()

    class Meta(base.WorkspaceBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBaseSerializer.Meta.fields,
            "team_members",
            "team_member_invites",
            "projects",
            "labels",
            "quota",
        )
