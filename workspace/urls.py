"""Workspace url patterns."""
from django.urls import (
    include,
    path,
)

from workspace.views.label import LabelCreate
from workspace.views.workspace_board import (
    WorkspaceBoardCreate,
    WorkspaceBoardRead,
)
from workspace.views.workspace_board_section import (
    WorkspaceBoardSectionCreate,
    WorkspaceBoardSectionMove,
    WorkspaceBoardSectionRead,
)

from . import (
    views,
)
from .views.task import (
    TaskCreate,
    TaskRetrieveUpdateDestroy,
)
from .views.workspace import (
    InviteUserToWorkspace,
    WorkspaceCreate,
    WorkspaceList,
    WorkspacePictureUploadView,
    WorkspaceRetrieve,
)
from .views.workspace_user import (
    WorkspaceUserDestroy,
)

app_name = "workspace"

workspace_board_patterns = (
    # Create
    path(
        "workspace-board",
        WorkspaceBoardCreate.as_view(),
        name="create",
    ),
    # Read
    path(
        "workspace-board/<uuid:workspace_board_uuid>",
        WorkspaceBoardRead.as_view(),
        name="read",
    ),
    # Update
    # Delete
)

workspace_board_section_patterns = (
    # Create
    path(
        "",
        WorkspaceBoardSectionCreate.as_view(),
        name="create",
    ),
    # Read
    path(
        "<uuid:workspace_board_section_uuid>",
        WorkspaceBoardSectionRead.as_view(),
        name="read",
    ),
    # Update
    # Delete
    # RPC
    path(
        "<uuid:workspace_board_section_uuid>/move",
        WorkspaceBoardSectionMove.as_view(),
        name="move",
    ),
)

label_patterns = (
    # Create
    path(
        "",
        LabelCreate.as_view(),
        name="create",
    ),
    # Read
    # Update
    # Delete
)

# TODO Rename all views to use standard CRUD terminology
urlpatterns = (
    # Workspace
    # Create
    path(
        "workspaces/",
        WorkspaceCreate.as_view(),
        name="workspace-create",
    ),
    # Read
    path(
        "user/workspaces/",
        WorkspaceList.as_view(),
        name="workspace-list",
    ),
    path(
        "workspace/<uuid:workspace_uuid>",
        WorkspaceRetrieve.as_view(),
        name="workspace",
    ),
    # Archived workspace boards
    path(
        "workspace/<uuid:workspace_uuid>/workspace-boards-archived/",
        views.WorkspaceBoardArchivedList.as_view(),
        name="workspace-boards-archived",
    ),
    # Update
    # Delete
    # RPC
    path(
        "workspace/<uuid:uuid>/picture-upload",
        WorkspacePictureUploadView.as_view(),
        name="workspace-picture-upload",
    ),
    path(
        "workspace/<uuid:uuid>/invite-user",
        InviteUserToWorkspace.as_view(),
        name="workspace-invite-user",
    ),
    # WorkspaceUser
    # Create
    # Read
    # Update
    # Delete
    path(
        "workspace-user/<uuid:uuid>",
        WorkspaceUserDestroy.as_view(),
        name="workspace-user-delete",
    ),
    # WorkspaceBoard
    path(
        "workspace-board/",
        include((workspace_board_patterns, "workspace-boards")),
    ),
    # WorkspaceBoardSection
    path(
        "workspace-board-section/",
        include(
            (workspace_board_section_patterns, "workspace-board-sections")
        ),
    ),
    # Task
    # Create
    path(
        # TODO should be "task/"
        "task",
        TaskCreate.as_view(),
        name="task-create",
    ),
    # Read, Update, Delete
    path(
        "task/<uuid:task_uuid>",
        TaskRetrieveUpdateDestroy.as_view(),
        name="task",
    ),
    # Label
    path("label/", include((label_patterns, "labels"))),
)
