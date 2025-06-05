# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Test views for email confirmation testing."""

import secrets

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from projectify.user.services.auth import user_sign_up
from projectify.user.services.internal import Token, user_make_token


def email_confirm_test(request: HttpRequest) -> HttpResponse:
    """
    Render a test page with links to test email confirmation.

    This view is only available in development mode and when the user is not logged in.
    """
    if not settings.DEBUG:
        return HttpResponse(
            "This page is only available in development mode", status=403
        )
    if request.user.is_authenticated:
        return HttpResponse(
            "You must be logged out to use this page", status=403
        )
    user = user_sign_up(
        email=f"test-email-confirm-{secrets.token_hex(16)}@localhost",
        password=secrets.token_hex(32),
        tos_agreed=True,
        privacy_policy_agreed=True,
    )
    user.is_active = False
    user.save()

    valid_token = user_make_token(user=user, kind="confirm_email_address")
    invalid_token = Token("invalid-token-12345")
    invalid_email = "nonexistent@example.com"

    # Generate URLs for the three scenarios
    valid_url = reverse(
        "users-django:confirm-email", args=(user.email, valid_token)
    )

    invalid_token_url = reverse(
        "users-django:confirm-email", args=(user.email, invalid_token)
    )

    invalid_email_url = reverse(
        "users-django:confirm-email", args=(invalid_email, valid_token)
    )

    context = {
        "valid_url": valid_url,
        "invalid_token_url": invalid_token_url,
        "invalid_email_url": invalid_email_url,
        "test_email": user.email,
        "valid_token": valid_token,
        "invalid_token": invalid_token,
        "invalid_email": invalid_email,
    }

    return render(request, "user/test_email_confirm.html", context=context)
