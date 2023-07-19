"""Workspace url patterns."""
from django.urls import (
    path,
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
        views.WorkspaceCreate.as_view(),
        name="workspace-create",
    ),
    # Read
    path(
        "user/workspaces/",
        views.WorkspaceList.as_view(),
        name="workspace-list",
    ),
    path(
        "workspace/<uuid:workspace_uuid>",
        views.WorkspaceRetrieve.as_view(),
        name="workspace",
    ),
    # Update
    path(
        "workspace/<uuid:uuid>/picture-upload",
        views.WorkspacePictureUploadView.as_view(),
        name="workspace-picture-upload",
    ),
    # Delete
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
    # Read
    path(
        "task/<uuid:task_uuid>",
        views.TaskRetrieve.as_view(),
        name="task",
    ),
    # Update
    # Delete
)
