"""User url patterns."""
from django.urls import (
    include,
    path,
)

from user.views import ProfilePictureUpload, UserRead

app_name = "user"

user_patterns = (
    path(
        "",
        UserRead.as_view(),
        name="read",
    ),
    path(
        "profile-picture/upload",
        ProfilePictureUpload.as_view(),
        name="upload-profile-picture",
    ),
)

urlpatterns = (path("user", include((user_patterns, "users"))),)
