# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Test URL patterns for email confirmation testing."""

from django.urls import path

from projectify.lib.settings import get_settings
from projectify.user.views.view_tests import email_confirm_test

settings = get_settings()
assert settings.DEBUG_AUTH, "Can't import this if DEBUG_AUTH isn't set"


urlpatterns = [
    path("email-confirm-test/", email_confirm_test),
]
