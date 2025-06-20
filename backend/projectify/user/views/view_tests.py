# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Test views for email confirmation testing."""

import secrets

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse

from projectify.lib.settings import get_settings
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.user.services.auth import user_sign_up
from projectify.user.services.internal import Token, user_make_token

settings = get_settings()
assert settings.DEBUG_AUTH, "Can't import this if DEBUG_AUTH isn't set"


def test_index(request: HttpRequest) -> HttpResponse:
    """
    Render an index page with links to all available test views.

    This view is only available in development mode.
    """
    if not settings.DEBUG_AUTH:
        return HttpResponseForbidden(
            "This page is only available in development mode"
        )

    return render(request, "user/test_index.html")


def email_confirm_test(request: HttpRequest) -> HttpResponse:
    """
    Render a test page with links to test email confirmation.

    This view is only available in development mode and when the user is not logged in.
    """
    if not settings.DEBUG_AUTH:
        return HttpResponseForbidden(
            "This page is only available in development mode"
        )
    if request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged out to use this page")
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


def password_reset_confirm_test(request: HttpRequest) -> HttpResponse:
    """
    Render a test page with links to password reset confirmation pages.

    This view is only available in development mode and when the user is not logged in.
    """
    if not settings.DEBUG_AUTH:
        return HttpResponseForbidden(
            "This page is only available in development mode"
        )
    if request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged out to use this page")
    user = user_sign_up(
        email=f"test-password-reset-confirm-{secrets.token_hex(16)}@localhost",
        password=secrets.token_hex(32),
        tos_agreed=True,
        privacy_policy_agreed=True,
    )
    user.is_active = True
    user.save()

    valid_token = user_make_token(user=user, kind="reset_password")
    invalid_token = Token("invalid-reset-token-12345")
    invalid_email = "nonexistent@example.com"

    # Generate URLs for the three scenarios
    valid_url = reverse(
        "users-django:confirm-password-reset", args=(user.email, valid_token)
    )

    invalid_token_url = reverse(
        "users-django:confirm-password-reset", args=(user.email, invalid_token)
    )

    invalid_email_url = reverse(
        "users-django:confirm-password-reset",
        args=(invalid_email, valid_token),
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

    return render(
        request, "user/test_password_reset_confirm.html", context=context
    )


@login_required
def email_update_confirm_test(
    request: AuthenticatedHttpRequest,
) -> HttpResponse:
    """
    Render a test page with links to test email address update confirmation.

    This view is only available in development mode and when the user is authenticated.
    It uses the current user to test email address update confirmation.
    """
    if not settings.DEBUG_AUTH:
        return HttpResponseForbidden(
            "This page is only available in development mode"
        )

    user = request.user
    old_email = user.email
    user.unconfirmed_email = user.email
    user.save()

    valid_token = user_make_token(user=user, kind="update_email_address")
    invalid_token = Token("invalid-token-67890")

    # Generate URLs for different scenarios
    valid_url = reverse(
        "users-django:confirm-email-address-update", args=(valid_token,)
    )

    invalid_url = reverse(
        "users-django:confirm-email-address-update", args=(invalid_token,)
    )

    context = {
        "user": user,
        "old_email": old_email,
        "new_email": user.unconfirmed_email,
        "valid_token": valid_token,
        "invalid_token": invalid_token,
        "valid_url": valid_url,
        "invalid_url": invalid_url,
    }

    return render(
        request, "user/test_email_update_confirm.html", context=context
    )
