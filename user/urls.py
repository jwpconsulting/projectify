"""Workspace url patterns."""
from django.urls import (
    path,
)

from . import (
    views,
)


app_name = "user"

urlpatterns = (
    path(
        r"profile-picture-upload",
        views.ProfilePictureUploadView.as_view(),
        name="profile-picture-upload",
    ),
)
