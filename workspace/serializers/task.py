"""Task serializers."""
from . import (
    base,
)


class TaskWithSubTaskSerializer(base.TaskBaseSerializer):
    """Serialize all task details."""

    labels = base.LabelBaseSerializer(many=True, read_only=True)
    assignee = base.WorkspaceUserBaseSerializer(read_only=True)
    sub_tasks = base.SubTaskBaseSerializer(
        many=True, read_only=True, source="subtask_set"
    )

    class Meta(base.TaskBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.TaskBaseSerializer.Meta.fields,
            "sub_tasks",
        )
