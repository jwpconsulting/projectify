"""Workspace url patterns."""
from django.urls import (
    path,
)

from workspace.views.task import (
    TaskCreate,
    TaskRetrieveUpdate,
)
from workspace.views.workspace import (
    InviteUserToWorkspace,
    WorkspaceCreate,
    WorkspaceList,
    WorkspacePictureUploadView,
    WorkspaceRetrieve,
)

from . import (
    views,
)


app_name = "workspace"

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
    # WorkspaceBoard
    # Create
    # Read
    path(
        "workspace-board/<uuid:workspace_board_uuid>",
        views.WorkspaceBoardRetrieve.as_view(),
        name="workspace-board",
    ),
    path(
        "workspace/<uuid:workspace_uuid>/workspace-boards-archived/",
        views.WorkspaceBoardArchivedList.as_view(),
        name="workspace-boards-archived",
    ),
    # Update
    # Delete
    # WorkspaceBoardSection
    # Create
    # Read
    path(
        "workspace-board-section/<uuid:workspace_board_section_uuid>",
        views.WorkspaceBoardSectionRetrieve.as_view(),
        name="workspace-board-section",
    ),
    # Update
    # Delete
    # Task
    # Create
    path(
        "task",
        TaskCreate.as_view(),
        name="task-create",
    ),
    # Read
    path(
        "task/<uuid:task_uuid>",
        TaskRetrieveUpdate.as_view(),
        name="task",
    ),
    # Update
    # Delete
)
