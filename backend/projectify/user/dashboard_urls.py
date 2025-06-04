# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""New user view URL patterns."""

from django.urls import path

from projectify.user.views.auth import (
    confirm_password_reset,
    log_in,
    log_out,
    request_password_reset,
    sign_up,
)
from projectify.user.views.user import (
    email_address_confirm,
    email_address_update,
    password_change,
    user_profile,
)

app_name = "users-django"

urlpatterns = (
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
