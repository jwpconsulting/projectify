# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""New user view URL patterns."""

from django.urls import path

from projectify.user.views.auth import (
    email_confirm,
    email_confirmation_link_sent,
    log_in,
    log_out,
    password_reset,
    password_reset_confirm,
    password_reset_request,
    password_reset_requested,
    sign_up,
)
from projectify.user.views.user import (
    email_address_update,
    email_address_update_confirm,
    email_address_update_confirmed,
    email_address_update_requested,
    password_change,
    user_profile,
)

app_name = "users"

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
        email_address_update_confirm,
        name="confirm-email-address-update",
    ),
    path(
        "profile/update-email-address/requested",
        email_address_update_requested,
        name="requested-email-address-update",
    ),
    path(
        "profile/update-email-address/confirmed",
        email_address_update_confirmed,
        name="confirmed-email-address-update",
    ),
    # auth views
    path("log-in", log_in, name="log-in"),
    path(
        "request-password-reset",
        password_reset_request,
        name="request-password-reset",
    ),
    path("sign-up", sign_up, name="sign-up"),
    path(
        "sent-email-confirmation-link",
        email_confirmation_link_sent,
        name="sent-email-confirmation-link",
    ),
    path(
        "confirm-email/<str:email>/<str:token>",
        email_confirm,
        name="confirm-email",
    ),
    path("log-out", log_out, name="log-out"),
    path(
        "confirm-password-reset/<str:email>/<str:token>",
        password_reset_confirm,
        name="confirm-password-reset",
    ),
    path(
        "requested-password-reset",
        password_reset_requested,
        name="requested-password-reset",
    ),
    path(
        "reset-password",
        password_reset,
        name="reset-password",
    ),
)
