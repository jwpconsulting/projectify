# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Test URL patterns for email confirmation testing."""

from django.urls import path

from projectify.lib.settings import get_settings
from projectify.user.views.view_tests import (
    email_confirm_test,
    email_update_confirm_test,
    password_reset_confirm_test,
    test_index,
)

settings = get_settings()
assert settings.DEBUG_AUTH, "Can't import this if DEBUG_AUTH isn't set"

app_name = "users-testing"


urlpatterns = [
    path("", test_index, name="test-index"),
    path("email-confirm-test/", email_confirm_test, name="email-confirm-test"),
    path(
        "email-update-confirm-test/",
        email_update_confirm_test,
        name="email-update-confirm-test",
    ),
    path(
        "confirm-password-reset-test/",
        password_reset_confirm_test,
        name="confirm-password-reset-test",
    ),
]
