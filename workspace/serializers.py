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


timestamps = (
    "created",
    "modified",
)

title_description = (
    "title",
    "description",
)


class WorkspaceUserSerializer(serializers.ModelSerializer):
    """Workspace user serializer."""

    user = user_serializers.UserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.WorkspaceUser
        fields = (
            *timestamps,
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


class SubTaskBaseSerializer(serializers.ModelSerializer):
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


class ChatMessageBaseSerializer(serializers.ModelSerializer):
    """ChatMessage model serializer."""

    author = WorkspaceUserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.ChatMessage
        fields = (
            *timestamps,
            "uuid",
            "text",
            "author",
        )


class TaskBaseSerializer(serializers.ModelSerializer):
    """Task model serializer."""

    labels = LabelSerializer(many=True, read_only=True)
    assignee = WorkspaceUserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.Task
        fields = (
            *timestamps,
            *title_description,
            "_order",
            "uuid",
            "deadline",
            "number",
            "labels",
            "assignee",
        )


class WorkspaceBaseSerializer(serializers.ModelSerializer):
    """Workspace base serializer."""

    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
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


class WorkspaceBoardBaseSerializer(serializers.ModelSerializer):
    """Workspace board base serializer."""

    class Meta:
        """Meta."""

        model = models.WorkspaceBoard
        fields = (
            *timestamps,
            *title_description,
            "deadline",
            "uuid",
            "archived",
        )


class WorkspaceBoardUpSerializer(WorkspaceBoardBaseSerializer):
    """Serialize workspace board up."""

    workspace = WorkspaceBaseSerializer(read_only=True)

    class Meta(WorkspaceBoardBaseSerializer.Meta):
        """Meta."""

        fields = (
            *WorkspaceBoardBaseSerializer.Meta.fields,
            "workspace",
        )


class WorkspaceBoardSectionBaseSerializer(serializers.ModelSerializer):
    """Workspace board section serializer."""

    class Meta:
        """Meta."""

        model = models.WorkspaceBoardSection
        fields = (
            *timestamps,
            *title_description,
            "_order",
            "uuid",
        )


class WorkspaceBoardSectionUpSerializer(WorkspaceBoardSectionBaseSerializer):
    """Serialize workspace board section up the hierarchy."""

    workspace_board = WorkspaceBoardUpSerializer(read_only=True)

    class Meta(WorkspaceBoardSectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *WorkspaceBoardSectionBaseSerializer.Meta.fields,
            "workspace_board",
        )


class TaskWithSubTaskSerializer(TaskBaseSerializer):
    """Serialize all task details."""

    sub_tasks = SubTaskBaseSerializer(
        many=True, read_only=True, source="subtask_set"
    )

    class Meta(TaskBaseSerializer.Meta):
        """Meta."""

        fields = (
            *TaskBaseSerializer.Meta.fields,
            "sub_tasks",
        )


class TaskDetailSerializer(TaskWithSubTaskSerializer):
    """Serialize all task details."""

    chat_messages = ChatMessageBaseSerializer(
        many=True, read_only=True, source="chatmessage_set"
    )
    workspace_board_section = WorkspaceBoardSectionUpSerializer(read_only=True)

    class Meta(TaskWithSubTaskSerializer.Meta):
        """Meta."""

        fields = (
            *TaskWithSubTaskSerializer.Meta.fields,
            "chat_messages",
            "workspace_board_section",
        )


class WorkspaceBoardSectionSerializer(WorkspaceBoardSectionBaseSerializer):
    """Workspace board section serializer."""

    tasks = TaskWithSubTaskSerializer(
        many=True, read_only=True, source="task_set"
    )

    class Meta(WorkspaceBoardSectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *WorkspaceBoardSectionBaseSerializer.Meta.fields,
            "tasks",
        )


class WorkspaceBoardSerializer(WorkspaceBoardBaseSerializer):
    """Workspace board serializer."""

    workspace_board_sections = WorkspaceBoardSectionSerializer(
        many=True, read_only=True, source="workspaceboardsection_set"
    )

    class Meta(WorkspaceBoardBaseSerializer.Meta):
        """Meta."""

        fields = (
            *WorkspaceBoardBaseSerializer.Meta.fields,
            "workspace_board_sections",
        )


class WorkspaceBoardDetailSerializer(WorkspaceBoardSerializer):
    """Workspace board serializer."""

    workspace = WorkspaceBaseSerializer(read_only=True)

    class Meta(WorkspaceBoardSerializer.Meta):
        """Meta."""

        fields = (
            *WorkspaceBoardSerializer.Meta.fields,
            "workspace",
        )


class WorkspaceBoardSectionDetailSerializer(WorkspaceBoardSectionSerializer):
    """Workspace board section serializer."""

    workspace_board = WorkspaceBoardBaseSerializer(read_only=True)

    class Meta(WorkspaceBoardSectionSerializer.Meta):
        """Meta."""

        fields = (
            *WorkspaceBoardSectionSerializer.Meta.fields,
            "workspace_board",
        )


class WorkspaceSerializer(WorkspaceBaseSerializer):
    """Workspace serializer."""

    workspace_users = WorkspaceUserSerializer(
        read_only=True, many=True, source="workspaceuser_set"
    )
    workspace_boards = WorkspaceBoardBaseSerializer(
        read_only=True, many=True, source="workspaceboard_set"
    )
    labels = LabelSerializer(read_only=True, many=True, source="label_set")

    class Meta(WorkspaceBaseSerializer.Meta):
        """Meta."""

        fields = (
            *WorkspaceBaseSerializer.Meta.fields,
            "workspace_users",
            "workspace_boards",
            "labels",
        )
