# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024,2026 JWP Consulting GK
"""User authentication views."""

import logging
from typing import Any

from django import forms
from django.contrib.auth.password_validation import (
    password_validators_help_texts,
)
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.base.provider import Provider
from django_ratelimit.core import UNSAFE, get_usage
from django_ratelimit.decorators import ratelimit

from projectify.lib.forms import populate_form_with_errors
from projectify.templatetags.projectify import anchor
from projectify.user.services.auth import (
    user_confirm_email,
    user_confirm_password_reset,
    user_log_in,
    user_log_out,
    user_request_password_reset,
    user_sign_up,
)
from projectify.user.services.internal import Token

logger = logging.getLogger(__name__)


def allauth_provider_info(request: HttpRequest) -> list[dict[str, str]]:
    """Format allauth socialaccount providers for log in and sign up."""
    result = []
    # Copied from get_providers in
    # allauth.socialaccount.templatetags.socialaccount
    adapter = get_adapter()  # type: ignore[no-untyped-call]
    providers: list[Provider] = adapter.list_providers(request)
    for provider in providers:
        if provider.app is None:
            continue
        # The original get_providers also checked the following:
        # if provider.uses_apps or provider.app.settings.get("hidden")
        # For Projectify's providers-GitHub, Google, and openid_connect for testing
        # this means that they won't show up
        slug = provider.get_slug()
        match slug:
            case "github":
                label = _("Log in with GitHub")
                alt = _("GitHub")
                icon = "user/login_with_github.svg"
            case "google":
                label = _("Log in with Google")
                alt = _("Google")
                icon = "user/login_with_google.svg"
            case "apple":
                label = _("Log in with Apple")
                alt = _("Apple")
                icon = "user/login_with_apple.svg"
            case "openid_connect":
                label = _("Dummy log in")
                alt = _("Dummy log in")
                icon = "heroicons/user.svg"
            case other:
                logger.error("Unrecognized auth provider %s", other)
                continue
        href = provider.get_login_url(request)
        result.append({"label": label, "alt": alt, "icon": icon, "href": href})
    return result


def log_out(request: HttpRequest) -> HttpResponse:
    """Log the user out. Need to be logged in first."""
    user = request.user
    if not user.is_anonymous:
        user_log_out(request=request)
    return redirect("/")


class SignUpForm(forms.Form):
    """Sign up form."""

    tos_agreed = forms.BooleanField()
    privacy_policy_agreed = forms.BooleanField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    email.widget.attrs.update({"placeholder": _("Enter your email")})
    password.widget.attrs.update({"placeholder": _("Enter your password")})

    def __init__(self, *args: Any, **kwargs: Any):
        """Override and add fields."""
        super().__init__(*args, **kwargs)
        self.fields["privacy_policy_agreed"].label = format_html(
            _("<span>I agree to the {privacy_policy_anchor}</span>"),
            privacy_policy_anchor=anchor(
                label=_("Privacy Policy"),
                href=reverse("storefront:privacy"),
                external=True,
            ),
        )
        self.fields["tos_agreed"].label = format_html(
            _("<span>I agree to the {tos_anchor}</span>"),
            tos_anchor=anchor(
                label=_("Terms of Service"),
                href=reverse("storefront:tos"),
                external=True,
            ),
        )


# No authentication required
@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="10/h", method=UNSAFE)
def sign_up(request: HttpRequest) -> HttpResponse:
    """Sign the user up."""
    match request.method:
        case "GET":
            form = SignUpForm()
            status = 200
        case "POST":
            # Originally, I wanted 4/h but there's a weird off-by-one issue here
            # See the comment below as well.
            # Solution:
            # ratelimit doesn't check based on a windowed rate count, but
            # how many times within a fixed window (e.g., hour 1, hour 2, etc.)
            # some action is performed
            # When your rate limit is 5 and hit this view 4 times
            # at the end of hour
            # 1, and hit it once the beginning of hour 2,
            # it would count the one hit of hour 2 as a separate windowed hit,
            # even though you've hit this view 5 times within one hour.
            #
            #      5 hits
            #      .------.
            #      v      v
            #  |   xxxx | x      |
            #  | hour 1 | hour 2 |
            #
            # This counts as 4 hits, and then 1 hit!
            # Justus 2026-04-16
            limit = get_usage(
                request,
                group="projectify.user.views.auth.sign_up",
                key="ip",
                rate="3/h",
                increment=False,
            )
            form = SignUpForm(request.POST)
            # Rate limit and show appropriate error message
            if limit and limit["should_limit"]:
                form.add_error(
                    field=None,
                    error=_("Too many sign up attempts. Slow down."),
                )
                status = 429
            elif form.is_valid():
                data = form.cleaned_data
                try:
                    user_sign_up(
                        email=data["email"],
                        password=data["password"],
                        tos_agreed=data["tos_agreed"],
                        privacy_policy_agreed=data["privacy_policy_agreed"],
                    )
                except ValidationError as error:
                    populate_form_with_errors(form, error)
                    status = 400
                else:
                    # Increment limit only on success
                    # When you log the output here using print(limit), it prints the following:
                    # {'count': 1, 'limit': 4, 'should_limit': False, 'time_left': 1800}
                    # {'count': 2, 'limit': 4, 'should_limit': False, 'time_left': 1799}
                    # {'count': 3, 'limit': 4, 'should_limit': False, 'time_left': 1799}
                    # {'count': 4, 'limit': 4, 'should_limit': False, 'time_left': 1799}
                    # {'count': 5, 'limit': 4, 'should_limit': True, 'time_left': 1799}
                    # My expectation is that it limits when count == limit == 4, but it doesn't
                    limit = get_usage(
                        request,
                        group="projectify.user.views.auth.sign_up",
                        key="ip",
                        rate="3/h",
                        increment=True,
                    )
                    return redirect("users:sent-email-confirmation-link")
            else:
                status = 400
        case other:
            raise RuntimeError(f"Bad method {other}")
    context = {
        "validators": password_validators_help_texts(),
        "allauth_providers": allauth_provider_info(request),
        "form": form,
    }
    return render(request, "user/sign_up.html", context=context, status=status)


def email_confirmation_link_sent(request: HttpRequest) -> HttpResponse:
    """Confirm sign up and tell user about confirmation email."""
    return render(request, "user/email_confirmation_link_sent.html")


# TODO use form
def email_confirm(
    request: HttpRequest, email: str, token: str
) -> HttpResponse:
    """Confirm a new user's email address."""
    token = Token(token)

    try:
        user_confirm_email(email=email, token=token)
        context = {}
    except ValidationError as e:
        match e.error_dict:
            case {"email": email_error}:
                token_error = None
            case {"token": token_error}:
                email_error = None
            case _:
                raise ValueError(
                    "Don't know how to handle ValidationError of type "
                    f"{type(e)}"
                ) from e
        context = {"email_error": email_error, "token_error": token_error}
    return render(request, "user/email_confirm.html", context=context)


class LogInForm(forms.Form):
    """Form for logging in."""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    email.widget.attrs.update({"placeholder": _("Enter your email")})
    password.widget.attrs.update({"placeholder": _("Enter your password")})

    def __init__(self, *args: Any, **kwargs: Any):
        """Override constructor."""
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = anchor(
            label=_("Forgot password"), href="users:request-password-reset"
        )


@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="5/m", method=UNSAFE)
def log_in(request: HttpRequest) -> HttpResponse:
    """Log the user in."""
    FAILED_GROUP = "projectify.user.views.auth.log_in.fail"
    FAILED_KEY = "post:email"
    FAILED_RATE = "4/h"

    user = request.user
    if not user.is_anonymous:
        # TODO show flash "You're already logged in. Want to log out? Go to log
        # out..."
        return redirect("users:profile")

    match request.method:
        case "GET":
            form = LogInForm()
            status = 200
        case "POST":
            limit = get_usage(
                request,
                group=FAILED_GROUP,
                key=FAILED_KEY,
                rate=FAILED_RATE,
                increment=False,
            )
            form = LogInForm(request.POST)
            if limit and limit["should_limit"]:
                form.add_error(
                    field=None, error=_("Too many log in attempts. Slow down.")
                )
                status = 429
            elif form.is_valid():
                try:
                    user_log_in(
                        email=form.cleaned_data["email"],
                        password=form.cleaned_data["password"],
                        request=request,
                    )
                except ValidationError as error:
                    populate_form_with_errors(form, error)
                    get_usage(
                        request,
                        group=FAILED_GROUP,
                        key=FAILED_KEY,
                        rate=FAILED_RATE,
                        increment=True,
                    )
                else:
                    next = request.GET.get(
                        "next", reverse("dashboard:dashboard")
                    )
                    return redirect(next)
                status = 400
            else:
                status = 400
        case other:
            raise RuntimeError(f"Bad method {other}")
    context = {
        "allauth_providers": allauth_provider_info(request),
        "form": form,
    }
    return render(request, "user/log_in.html", context=context, status=status)


class PasswordResetRequestForm(forms.Form):
    """Form for requesting a password reset."""

    email = forms.EmailField()
    email.widget.attrs.update({"placeholder": _("Enter your email")})


@require_http_methods(["GET", "POST"])
@ratelimit(key="post:email", rate="5/h")
@ratelimit(key="ip", rate="5/h")
def password_reset_request(request: HttpRequest) -> HttpResponse:
    """Request a password reset."""
    match request.method:
        case "GET":
            form = PasswordResetRequestForm()
            status = 200
        case "POST":
            form = PasswordResetRequestForm(request.POST)
            if form.is_valid():
                try:
                    user_request_password_reset(
                        email=form.cleaned_data["email"]
                    )
                except ValidationError as error:
                    populate_form_with_errors(form, error)
                else:
                    return redirect("users:requested-password-reset")
            status = 400
        case other:
            raise RuntimeError(f"Called with method {other}")
    return render(
        request,
        "user/password_reset_request.html",
        context={"form": form},
        status=status,
    )


def password_reset_requested(request: HttpRequest) -> HttpResponse:
    """Confirm that user has requested a password reset."""
    return render(request, "user/password_reset_requested.html")


class PasswordResetConfirmForm(forms.Form):
    """Form to take in new password for user."""

    new_password = forms.CharField(
        label=_("New password"), widget=forms.PasswordInput
    )
    new_password_confirm = forms.CharField(
        label=_("Confirm new password"), widget=forms.PasswordInput
    )

    new_password.widget.attrs.update({"placeholder": _("Enter new password")})
    new_password_confirm.widget.attrs.update(
        {"placeholder": _("Confirm new password")}
    )


@require_http_methods(["GET", "POST"])
def password_reset_confirm(
    request: HttpRequest, email: str, token: str
) -> HttpResponse:
    """Confirm a password reset request and set a new password."""
    token = Token(token)
    match request.method:
        case "GET":
            form = PasswordResetConfirmForm()
            status = 200
        case _:
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                try:
                    user_confirm_password_reset(
                        email=email,
                        token=token,
                        new_password=form.cleaned_data["new_password"],
                        new_password_confirm=form.cleaned_data[
                            "new_password_confirm"
                        ],
                    )
                except ValidationError as error:
                    populate_form_with_errors(form, error)
                else:
                    return redirect("users:reset-password")
            status = 400
    return render(
        request,
        "user/password_reset_confirm.html",
        context={"validators": password_validators_help_texts(), "form": form},
        status=status,
    )


def password_reset(request: HttpRequest) -> HttpResponse:
    """Notify the user that they have changed their password."""
    return render(request, "user/password_reset.html")
