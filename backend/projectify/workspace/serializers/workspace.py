# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Workspace serializers."""

from rest_framework import serializers

from projectify.user.serializers import UserSerializer
from projectify.workspace.models.project import Project
from projectify.workspace.models.team_member import TeamMember

from . import base


class TeamMemberInviteSerializer(serializers.Serializer):
    """Serializer team member invites."""

    email = serializers.EmailField(source="user_invite.email")
    created = serializers.DateTimeField()


class WorkspaceTeamMemberSerializer(serializers.ModelSerializer[TeamMember]):
    """Workspace team member serializer."""

    user = UserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = TeamMember
        fields = (
            "user",
            "uuid",
            "role",
            "job_title",
        )
        extra_kwargs = {
            "role": {"required": True},
            "job_title": {"required": True},
        }


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


class WorkspaceProjectSerializer(serializers.ModelSerializer[Project]):
    """Serialize a single project."""

    class Meta:
        """Meta."""

        model = Project
        fields = (
            "title",
            "description",
            "uuid",
            "archived",
        )


class WorkspaceDetailSerializer(base.WorkspaceBaseSerializer):
    """
    Workspace detail serializer.

    Serializers ws board as well, but not the sections and so forth that they
    contain.
    """

    team_members = WorkspaceTeamMemberSerializer(
        read_only=True, many=True, source="teammember_set"
    )
    team_member_invites = TeamMemberInviteSerializer(
        read_only=True, many=True, source="teammemberinvite_set"
    )
    projects = WorkspaceProjectSerializer(
        read_only=True, many=True, source="project_set"
    )
    labels = base.LabelBaseSerializer(
        read_only=True, many=True, source="label_set"
    )
    quota = WorkspaceQuotaSerializer()

    class Meta(base.WorkspaceBaseSerializer.Meta):
        """Meta."""

        fields = (
            "uuid",
            "title",
            "description",
            "picture",
            "team_members",
            "team_member_invites",
            "projects",
            "labels",
            "quota",
        )
