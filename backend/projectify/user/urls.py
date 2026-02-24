# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""User url patterns."""

from django.urls import include, path

from projectify.user.views.user import (
    ChangePassword,
    ConfirmEmailAddressUpdate,
    ProfilePictureUpload,
    RequestEmailAddressUpdate,
    UserRead,
    UserUpdate,
)

app_name = "user"


user_patterns = (
    # Create
    # Read
    path(
        "current-user",
        UserRead.as_view(),
        name="read",
    ),
    # Update
    path(
        "current-user/update",
        UserUpdate.as_view(),
        name="update",
    ),
    # Delete
    # RPC
    path(
        "profile-picture/upload",
        ProfilePictureUpload.as_view(),
        name="upload-profile-picture",
    ),
    path(
        "change-password",
        ChangePassword.as_view(),
        name="change-password",
    ),
    path(
        "email-address-update/request",
        RequestEmailAddressUpdate.as_view(),
        name="request-email-address-update",
    ),
    path(
        "email-address-update/confirm",
        ConfirmEmailAddressUpdate.as_view(),
        name="confirm-email-address-update",
    ),
)

urlpatterns = (path("user/", include((user_patterns, "users"))),)
