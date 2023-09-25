"""Workspace app serializers."""
from .base import (
    WorkspaceBaseSerializer,
    WorkspaceBoardBaseSerializer,
)
from .task_detail import (
    TaskDetailSerializer,
    TaskUpdateSerializer,
)
from .workspace import (
    WorkspaceDetailSerializer,
)
from .workspace_board import (
    WorkspaceBoardDetailSerializer,
)
from .workspace_board_section import (
    WorkspaceBoardSectionDetailSerializer,
)


# XXX
# I don't like that we user the Base serializer here
__all__ = [
    "TaskDetailSerializer",
    "TaskUpdateSerializer",
    "WorkspaceBaseSerializer",
    "WorkspaceBoardBaseSerializer",
    "WorkspaceBoardDetailSerializer",
    "WorkspaceBoardSectionDetailSerializer",
    "WorkspaceDetailSerializer",
]