"""Workspace url patterns."""
from django.urls import (
    path,
)

from . import (
    views,
)


app_name = "workspace"

urlpatterns = (
    path(
        "workspace/<uuid:uuid>/picture-upload",
        views.WorkspacePictureUploadView.as_view(),
        name="workspace-picture-upload",
    ),
    path(
        "workspace-board/<uuid:workspace_board_uuid>",
        views.WorkspaceBoardRetrieve.as_view(),
        name="workspace-board",
    ),
    path(
        "workspace/<uuid:workspace_uuid>",
        views.WorkspaceRetrieve.as_view(),
        name="workspace",
    ),
    path(
        "workspace/<uuid:workspace_uuid>/workspace-boards-archived/",
        views.WorkspaceBoardArchivedList.as_view(),
        name="workspace-boards-archived",
    ),
)
