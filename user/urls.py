"""User url patterns."""
from django.urls import (
    include,
    path,
)

from user.views.user import (
    ConfirmEmail,
    LogIn,
    LogOut,
    PasswordResetConfirm,
    PasswordResetRequest,
    ProfilePictureUpload,
    SignUp,
    UserReadUpdate,
)

app_name = "user"

user_patterns = (
    # Create
    # Read + Update
    path(
        "current-user",
        UserReadUpdate.as_view(),
        name="read-update",
    ),
    # Delete
    # RPC
    path(
        "profile-picture/upload",
        ProfilePictureUpload.as_view(),
        name="upload-profile-picture",
    ),
    path(
        "log-out",
        LogOut.as_view(),
        name="log-out",
    ),
    # The following urls do not require being authenticated
    path(
        "sign-up",
        SignUp.as_view(),
        name="sign-up",
    ),
    path(
        "confirm-email",
        ConfirmEmail.as_view(),
        name="confirm-email",
    ),
    path(
        "log-in",
        LogIn.as_view(),
        name="log-in",
    ),
    path(
        "request-password-reset",
        PasswordResetRequest.as_view(),
        name="request-password-reset",
    ),
    path(
        "confirm-password-reset",
        PasswordResetConfirm.as_view(),
        name="confirm-password-reset",
    ),
)

urlpatterns = (path("user/", include((user_patterns, "users"))),)
