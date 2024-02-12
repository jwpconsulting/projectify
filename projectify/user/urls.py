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

from projectify.user.views.user import (
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
