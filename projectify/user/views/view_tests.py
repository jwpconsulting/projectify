# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025-2026 JWP Consulting GK
"""Test views for email confirmation testing."""

import secrets

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialLogin
from allauth.socialaccount.providers.openid_connect.provider import (
    OpenIDConnectProvider,
)

from projectify.lib.settings import get_settings
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.user.models import User
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


@require_http_methods(["POST"])
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
    valid_url = reverse("users:confirm-email", args=(user.email, valid_token))

    invalid_token_url = reverse(
        "users:confirm-email", args=(user.email, invalid_token)
    )

    invalid_email_url = reverse(
        "users:confirm-email", args=(invalid_email, valid_token)
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


@require_http_methods(["POST"])
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
        "users:confirm-password-reset", args=(user.email, valid_token)
    )

    invalid_token_url = reverse(
        "users:confirm-password-reset", args=(user.email, invalid_token)
    )

    invalid_email_url = reverse(
        "users:confirm-password-reset",
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
@require_http_methods(["POST"])
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
        "users:confirm-email-address-update", args=(valid_token,)
    )

    invalid_url = reverse(
        "users:confirm-email-address-update", args=(invalid_token,)
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


@require_http_methods(["GET", "POST"])
def socialaccount_signup_test(request: HttpRequest) -> HttpResponse:
    """
    Test the allauth socialaccount signup flow.

    Simulates two scenarios.
    Scenario a., new user
    Set up
    1. User already has account with IdP X and email A.
    2. They don't have an account on Projectify.

    Steps
    1. User signs up on Projectify using IdP X
    2. They are prompted to agree with TOS/privacy policy on Projectify
    3. They now have an account on Projectify with email A
    4. They can now log in on Projectify using IdP X
    """
    if not settings.DEBUG_AUTH:
        return HttpResponseForbidden(
            "This page is only available in development mode"
        )

    if request.method == "GET":
        return render(request, "user/test_socialaccount_signup.html")

    if request.user.is_authenticated:
        return HttpResponseForbidden(
            "You must be logged out to test this scenario"
        )

    # Synthetic apps created in
    # DefaultSocialAccountAdapter:list_apps()
    # https://github.com/pennersr/django-allauth/blob/cf7f55d79e421e5d5ba078e31119a799f8b149e8/allauth/socialaccount/adapter.py#L262
    app = SocialApp(provider="openid_connect", client_id="test.id")
    provider = OpenIDConnectProvider(request, app=app)  # type: ignore

    match request.POST.get("scenario"):
        case "new_user":
            test_email = f"test-new-{secrets.token_hex(8)}@example.com"
            user = User(email=test_email)
            user.set_unusable_password()
            mock_account = SocialAccount(
                provider=app.provider,
                uid=secrets.token_hex(8),
                extra_data={"email": test_email},
            )
        case "existing_user":
            test_email = f"test-existing-{secrets.token_hex(8)}@example.com"
            user_sign_up(
                email=test_email,
                password=secrets.token_hex(32),
                tos_agreed=True,
                privacy_policy_agreed=True,
            )
            user = User(email=test_email)
            user.set_unusable_password()
            mock_account = SocialAccount(
                provider=app.provider,
                uid=secrets.token_hex(8),
                extra_data={
                    "email": test_email,
                    # XXX log in needed?
                    "login": f"testuser{secrets.token_hex(4)}",
                },
            )
            # TODO fix
            # MultipleObjectsReturned at /user/auth/signup/
        case _:
            return HttpResponseForbidden("Invalid scenario")
    sociallogin = SocialLogin(
        user=user, account=mock_account, provider=provider
    )
    request.session["socialaccount_sociallogin"] = sociallogin.serialize()
    return redirect("socialaccount_signup")
