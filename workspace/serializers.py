"""Workspace app serializers."""
from typing import (
    Iterable,
    Optional,
)

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


class WorkspaceUserSerializer(
    serializers.ModelSerializer[models.WorkspaceUser]
):
    """Workspace user serializer."""

    user = user_serializers.UserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.WorkspaceUser
        fields: Iterable[str] = (
            *timestamps,
            "user",
            "uuid",
            "role",
            "job_title",
        )


class LabelSerializer(serializers.ModelSerializer[models.Label]):
    """Label model serializer."""

    class Meta:
        """Meta."""

        model = models.Label
        fields: Iterable[str] = (
            "name",
            "color",
            "uuid",
        )


class SubTaskBaseSerializer(serializers.ModelSerializer[models.SubTask]):
    """SubTask model serializer."""

    class Meta:
        """Meta."""

        model = models.SubTask
        fields: Iterable[str] = (
            *timestamps,
            *title_description,
            "uuid",
            "done",
            "_order",
        )


class ChatMessageBaseSerializer(
    serializers.ModelSerializer[models.ChatMessage]
):
    """ChatMessage model serializer."""

    author = WorkspaceUserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.ChatMessage
        fields: Iterable[str] = (
            *timestamps,
            "uuid",
            "text",
            "author",
        )


class TaskBaseSerializer(serializers.ModelSerializer[models.Task]):
    """Task model serializer."""

    labels = LabelSerializer(many=True, read_only=True)
    assignee = WorkspaceUserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = models.Task
        read_only_fields = ("number",)
        fields: Iterable[str] = (
            *timestamps,
            *title_description,
            "_order",
            "uuid",
            "deadline",
            "number",
            "labels",
            "assignee",
        )


class WorkspaceBaseSerializer(serializers.ModelSerializer[models.Workspace]):
    """Workspace base serializer."""

    picture = serializers.SerializerMethodField()

    def get_picture(self, obj: models.Workspace) -> Optional[str]:
        """Return profile picture."""
        return utils.crop_image(obj.picture, 100, 100)

    class Meta:
        """Meta."""

        model = models.Workspace
        fields: Iterable[str] = (
            *timestamps,
            *title_description,
            "uuid",
            "picture",
        )


class WorkspaceBoardBaseSerializer(
    serializers.ModelSerializer[models.WorkspaceBoard]
):
    """Workspace board base serializer."""

    class Meta:
        """Meta."""

        model = models.WorkspaceBoard
        fields: Iterable[str] = (
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

        fields: Iterable[str] = (
            *WorkspaceBoardBaseSerializer.Meta.fields,
            "workspace",
        )


class WorkspaceBoardSectionBaseSerializer(
    serializers.ModelSerializer[models.WorkspaceBoard]
):
    """Workspace board section serializer."""

    class Meta:
        """Meta."""

        model = models.WorkspaceBoardSection
        fields: Iterable[str] = (
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

        fields: Iterable[str] = (
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

        fields: Iterable[str] = (
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

        fields: Iterable[str] = (
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

        fields: Iterable[str] = (
            *WorkspaceBoardBaseSerializer.Meta.fields,
            "workspace_board_sections",
        )


class WorkspaceBoardDetailSerializer(WorkspaceBoardSerializer):
    """Workspace board serializer."""

    workspace = WorkspaceBaseSerializer(read_only=True)

    class Meta(WorkspaceBoardSerializer.Meta):
        """Meta."""

        fields: Iterable[str] = (
            *WorkspaceBoardSerializer.Meta.fields,
            "workspace",
        )


class WorkspaceBoardSectionDetailSerializer(WorkspaceBoardSectionSerializer):
    """Workspace board section serializer."""

    workspace_board = WorkspaceBoardUpSerializer(read_only=True)

    class Meta(WorkspaceBoardSectionSerializer.Meta):
        """Meta."""

        fields: Iterable[str] = (
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

        fields: Iterable[str] = (
            *WorkspaceBaseSerializer.Meta.fields,
            "workspace_users",
            "workspace_boards",
            "labels",
        )
