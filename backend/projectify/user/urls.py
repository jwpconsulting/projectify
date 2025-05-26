# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""User url patterns."""

from django.urls import include, path

from projectify.user.views.auth import (
    ConfirmEmail,
    LogIn,
    LogOut,
    PasswordPolicyRead,
    PasswordResetConfirm,
    PasswordResetRequest,
    SignUp,
    confirm_password_reset,
    log_in,
    log_out,
    request_password_reset,
    sign_up,
)
from projectify.user.views.user import (
    ChangePassword,
    ConfirmEmailAddressUpdate,
    ProfilePictureUpload,
    RequestEmailAddressUpdate,
    UserRead,
    UserUpdate,
    email_address_confirm,
    email_address_update,
    password_change,
    user_profile,
)

app_name = "user"

user_patterns_django = (
    path("profile/", user_profile, name="profile"),
    path("profile/change-password", password_change, name="change-password"),
    path(
        "profile/update-email-address/",
        email_address_update,
        name="update-email-address",
    ),
    path(
        "profile/update-email-address/confirm/<str:token>",
        email_address_confirm,
        name="confirm-email-address",
    ),
    # auth views
    path("log-in", log_in, name="log-in"),
    path(
        "request-password-reset",
        request_password_reset,
        name="request-password-reset",
    ),
    path("sign-up", sign_up, name="sign-up"),
    path("log-out", log_out, name="log-out"),
    path(
        "confirm-password-reset",
        confirm_password_reset,
        name="confirm-password-reset",
    ),
)

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

auth_patterns = (
    # Auth
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
    path(
        "password-policy",
        PasswordPolicyRead.as_view(),
        name="password-policy",
    ),
)

urlpatterns = (
    path("", include((user_patterns_django, "users-django"))),
    path("user/", include((user_patterns, "users"))),
    path("user/", include((auth_patterns, "auth"))),
)
