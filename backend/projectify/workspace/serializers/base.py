# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
            *timestamps,
            "user",
            "uuid",
            "role",
            "job_title",
        )
        extra_kwargs = {
            "job_title": {"required": True},
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
            "archived",
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
