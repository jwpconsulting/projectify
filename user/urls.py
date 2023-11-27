"""User url patterns."""
from django.urls import (
    include,
    path,
)

from user.views.user import ProfilePictureUpload, UserReadUpdate

app_name = "user"

user_patterns = (
    path(
        "",
        UserReadUpdate.as_view(),
        name="read-update",
    ),
    path(
        "profile-picture/upload",
        ProfilePictureUpload.as_view(),
        name="upload-profile-picture",
    ),
)

urlpatterns = (path("user", include((user_patterns, "users"))),)
