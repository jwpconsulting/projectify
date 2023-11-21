"""Workspace url patterns."""
from django.urls import (
    path,
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
)
