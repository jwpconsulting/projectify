"""Workspace url patterns."""
from django.urls import (
    include,
    path,
)

from workspace.views.label import LabelCreate
from workspace.views.workspace_board import (
    WorkspaceBoardCreate,
    WorkspaceBoardReadUpdate,
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
    TaskMove,
    TaskRetrieveUpdateDestroy,
)
from .views.workspace import (
    InviteUserToWorkspace,
    WorkspaceCreate,
    WorkspaceList,
    WorkspacePictureUploadView,
    WorkspaceReadUpdate,
)
from .views.workspace_user import (
    WorkspaceUserReadUpdateDelete,
)

app_name = "workspace"

workspace_patterns = (
    # Read + Update
    path(
        "<uuid:workspace_uuid>/",
        WorkspaceReadUpdate.as_view(),
        name="read-update",
    ),
)

workspace_user_patterns = (
    # Read + Update + Destroy
    path(
        "<uuid:workspace_user_uuid>/",
        WorkspaceUserReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
)

workspace_board_patterns = (
    # Create
    path(
        "workspace-board",
        WorkspaceBoardCreate.as_view(),
        name="create",
    ),
    # Read + Update
    path(
        "workspace-board/<uuid:workspace_board_uuid>",
        WorkspaceBoardReadUpdate.as_view(),
        name="read-update",
    ),
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

task_patterns = (
    # RPC
    path(
        "<uuid:task_uuid>/move",
        TaskMove.as_view(),
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
    path(
        "workspace/",
        include((workspace_patterns, "workspaces")),
    ),
    # TODO put the below paths into workspace_patterns as well
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
    path(
        "workspace-user/",
        include((workspace_user_patterns, "workspace-users")),
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
    path(
        "task/",
        include((task_patterns, "tasks")),
    ),
    # TODO put into task_patterns
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
