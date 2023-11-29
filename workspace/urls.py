"""Workspace url patterns."""
from django.urls import (
    include,
    path,
)

from workspace.views.label import LabelCreate, LabelUpdateDelete
from workspace.views.workspace_board import (
    WorkspaceBoardCreate,
    WorkspaceBoardReadUpdateDelete,
)
from workspace.views.workspace_board_section import (
    WorkspaceBoardSectionCreate,
    WorkspaceBoardSectionMove,
    WorkspaceBoardSectionReadUpdateDelete,
)

from . import (
    views,
)
from .views.task import (
    TaskCreate,
    TaskMoveAfterTask,
    TaskMoveToWorkspaceBoardSection,
    TaskRetrieveUpdateDelete,
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
        "<uuid:workspace_uuid>",
        WorkspaceReadUpdate.as_view(),
        name="read-update",
    ),
)

workspace_user_patterns = (
    # Read + Update + Destroy
    path(
        "<uuid:workspace_user_uuid>",
        WorkspaceUserReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
)

workspace_board_patterns = (
    # Create
    path(
        "",
        WorkspaceBoardCreate.as_view(),
        name="create",
    ),
    # Read + Update + Delete
    path(
        "<uuid:workspace_board_uuid>",
        WorkspaceBoardReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
)

workspace_board_section_patterns = (
    # Create
    path(
        "",
        WorkspaceBoardSectionCreate.as_view(),
        name="create",
    ),
    # Read + Update + Delete
    path(
        "<uuid:workspace_board_section_uuid>",
        WorkspaceBoardSectionReadUpdateDelete.as_view(),
        name="read-update-delete",
    ),
    # RPC
    path(
        "<uuid:workspace_board_section_uuid>/move",
        WorkspaceBoardSectionMove.as_view(),
        name="move",
    ),
)

task_patterns = (
    # Read, Update, Delete
    path(
        "<uuid:task_uuid>",
        TaskRetrieveUpdateDelete.as_view(),
        name="read-update-delete",
    ),
    # RPC
    path(
        "<uuid:task_uuid>/move-to-workspace-board-section",
        TaskMoveToWorkspaceBoardSection.as_view(),
        name="move-to-workspace-board-section",
    ),
    path(
        "<uuid:task_uuid>/move-after-task",
        TaskMoveAfterTask.as_view(),
        name="move-after-task",
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
    path(
        "<uuid:label_uuid>",
        LabelUpdateDelete.as_view(),
        name="update-delete",
    ),
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
    # Label
    path("label/", include((label_patterns, "labels"))),
)
