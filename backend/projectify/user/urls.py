# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""User url patterns."""

from django.urls import (
    include,
    path,
)

from projectify.user.views.auth import (
    ConfirmEmail,
    LogIn,
    LogOut,
    PasswordPolicyRead,
    PasswordResetConfirm,
    PasswordResetRequest,
    SignUp,
)
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
    path("user/", include((user_patterns, "users"))),
    path("user/", include((auth_patterns, "auth"))),
)
