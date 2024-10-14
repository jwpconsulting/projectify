# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""
Common values used in serializers. Contains all base serializers.

We define base serializer as a serializer that does not serialize
related model fields, and thus will not cause circular import issues.
"""

from collections.abc import (
    Sequence,
)
from typing import (
    Optional,
)

from rest_framework import (
    serializers,
)

from projectify import (
    utils,
)
from projectify.user import serializers as user_serializers

from .. import (
    models,
)

timestamps: Sequence[str] = (
    "created",
    "modified",
)

title_description: Sequence[str] = (
    "title",
    "description",
)


class UuidObjectSerializer(serializers.Serializer):
    """Deserialize the UUID for a any object with a UUID."""

    uuid = serializers.UUIDField()


class WorkspaceBaseSerializer(serializers.ModelSerializer[models.Workspace]):
    """Workspace base serializer."""

    picture = serializers.SerializerMethodField()

    def get_picture(self, obj: models.Workspace) -> Optional[str]:
        """Return profile picture."""
        return utils.crop_image(obj.picture, 100, 100)

    class Meta:
        """Meta."""

        model = models.Workspace
        fields = (
            *timestamps,
            *title_description,
            "uuid",
            "picture",
        )
        extra_kwargs = {
            "description": {"required": True},
        }


class TeamMemberBaseSerializer(serializers.ModelSerializer[models.TeamMember]):
    """Team member serializer."""

    user = user_serializers.UserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.TeamMember
        fields = (
            "user",
            "uuid",
            "role",
        )
        extra_kwargs = {
            "role": {"required": True},
        }


class ProjectBaseSerializer(serializers.ModelSerializer[models.Project]):
    """Project base serializer."""

    class Meta:
        """Meta."""

        model = models.Project
        fields = (
            *timestamps,
            *title_description,
            "due_date",
            "uuid",
        )
        extra_kwargs = {
            "due_date": {"required": True},
            "archived": {"required": True},
            "description": {"required": True},
        }


class SectionBaseSerializer(serializers.ModelSerializer[models.Section]):
    """Section serializer."""

    class Meta:
        """Meta."""

        model = models.Section
        fields = (
            *timestamps,
            *title_description,
            "_order",
            "uuid",
        )
        extra_kwargs = {
            "description": {"required": True},
        }


class TaskBaseSerializer(serializers.ModelSerializer[models.Task]):
    """Task model serializer."""

    class Meta:
        """Meta."""

        model = models.Task
        read_only_fields = ("number",)
        fields: Sequence[str] = (
            *timestamps,
            *title_description,
            "_order",
            "uuid",
            "due_date",
            "number",
        )
        extra_kwargs = {
            "due_date": {"required": True},
            "description": {"required": True},
        }


class ChatMessageBaseSerializer(
    serializers.ModelSerializer[models.ChatMessage]
):
    """ChatMessage model serializer."""

    # TODO remove, so that we can get rid of TeamMemberBaseSerializer
    author = TeamMemberBaseSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.ChatMessage
        fields = (
            *timestamps,
            "uuid",
            "text",
            "author",
        )


class SubTaskBaseSerializer(serializers.ModelSerializer[models.SubTask]):
    """SubTask model serializer."""

    class Meta:
        """Meta."""

        model = models.SubTask
        fields = (
            *timestamps,
            *title_description,
            "uuid",
            "done",
            "_order",
        )
        extra_kwargs = {
            "description": {"required": True},
            "done": {"required": True},
        }


class LabelBaseSerializer(serializers.ModelSerializer[models.Label]):
    """Label model serializer."""

    class Meta:
        """Meta."""

        model = models.Label
        fields = (
            "name",
            "color",
            "uuid",
        )
