"""Workspace app serializers."""
from rest_framework import (
    serializers,
)

from projectify import (
    utils,
)
from user import serializers as user_serializers

from . import (
    models,
)


class WorkspaceUserSerializer(serializers.ModelSerializer):
    """Workspace user serializer."""

    user = user_serializers.UserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.WorkspaceUser
        fields = (
            "user",
            "uuid",
            "role",
            "job_title",
        )


class LabelSerializer(serializers.ModelSerializer):
    """Label model serializer."""

    class Meta:
        """Meta."""

        model = models.Label
        fields = (
            "name",
            "color",
            "uuid",
        )


class TaskSerializer(serializers.ModelSerializer):
    """Task model serializer."""

    labels = LabelSerializer(many=True, read_only=True)
    assignee = WorkspaceUserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.Task
        fields = (
            "_order",
            "uuid",
            "title",
            "description",
            "deadline",
            "number",
            "labels",
            "assignee",
        )


class WorkspaceBoardSectionSerializer(serializers.ModelSerializer):
    """Workspace board section serializer."""

    tasks = TaskSerializer(many=True, read_only=True, source="task_set")

    class Meta:
        """Meta."""

        model = models.WorkspaceBoardSection
        fields = (
            "title",
            "description",
            "_order",
            "uuid",
            "tasks",
        )


class WorkspaceBoardSerializer(serializers.ModelSerializer):
    """Workspace board serializer."""

    workspace_board_sections = WorkspaceBoardSectionSerializer(
        many=True, read_only=True, source="workspaceboardsection_set"
    )

    class Meta:
        """Meta."""

        model = models.WorkspaceBoard
        fields = (
            "title",
            "description",
            "deadline",
            "uuid",
            "workspace_board_sections",
        )


class WorkspaceSerializer(serializers.ModelSerializer):
    """Workspace serializer."""

    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        """Return profile picture."""
        return utils.crop_image(obj.picture, 100, 100)

    class Meta:
        """Meta."""

        model = models.Workspace
        fields = (
            "uuid",
            "picture",
        )
