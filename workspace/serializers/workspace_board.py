"""Workspace board serializers."""
from workspace.serializers.task import (
    TaskWithSubTaskSerializer,
)

from . import (
    base,
)


class WorkspaceBoardSectionSerializer(
    base.WorkspaceBoardSectionBaseSerializer
):
    """
    Workspace board section serializer.

    Serializers the tasks that it contains.
    """

    tasks = TaskWithSubTaskSerializer(
        many=True, read_only=True, source="task_set"
    )

    class Meta(base.WorkspaceBoardSectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBoardSectionBaseSerializer.Meta.fields,
            "tasks",
        )


class WorkspaceBoardDetailSerializer(base.WorkspaceBoardBaseSerializer):
    """
    Workspace board serializer.

    Serializes in both directions, workspace and sections, including their
    tasks.
    """

    workspace_board_sections = WorkspaceBoardSectionSerializer(
        many=True, read_only=True, source="workspaceboardsection_set"
    )

    workspace = base.WorkspaceBaseSerializer(read_only=True)

    class Meta(base.WorkspaceBoardBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBoardBaseSerializer.Meta.fields,
            "workspace_board_sections",
            "workspace",
        )
