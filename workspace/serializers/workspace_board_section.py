"""Workspace board section serializers."""
from workspace.serializers.task import (
    TaskWithSubTaskSerializer,
)

from . import (
    base,
)


class WorkspaceBoardUpSerializer(base.WorkspaceBoardBaseSerializer):
    """
    Serialize workspace board and workspace containing it.

    Used when serializing up from a task or ws board section.
    """

    workspace = base.WorkspaceBaseSerializer(read_only=True)

    class Meta(base.WorkspaceBoardBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBoardBaseSerializer.Meta.fields,
            "workspace",
        )


class WorkspaceBoardSectionUpSerializer(
    base.WorkspaceBoardSectionBaseSerializer
):
    """Serialize workspace board section up the hierarchy."""

    workspace_board = WorkspaceBoardUpSerializer(read_only=True)

    class Meta(base.WorkspaceBoardSectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBoardSectionBaseSerializer.Meta.fields,
            "workspace_board",
        )


class WorkspaceBoardSectionDetailSerializer(
    base.WorkspaceBoardSectionBaseSerializer
):
    """
    Workspace board section detail serializer.

    Goes both up (to workspace) and down (all tasks).
    """

    workspace_board = WorkspaceBoardUpSerializer(read_only=True)
    tasks = TaskWithSubTaskSerializer(
        many=True, read_only=True, source="task_set"
    )

    class Meta(base.WorkspaceBoardSectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBoardSectionBaseSerializer.Meta.fields,
            "workspace_board",
            "tasks",
        )
