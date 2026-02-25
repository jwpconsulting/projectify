# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""User authentication views."""

from typing import Any

from django import forms
from django.contrib.auth.password_validation import (
    password_validators_help_texts,
)
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from django_ratelimit.core import UNSAFE, get_usage
from django_ratelimit.decorators import ratelimit
from rest_framework.exceptions import ValidationError

from projectify.lib.forms import populate_form_with_drf_errors
from projectify.user.services.auth import (
    user_confirm_email,
    user_confirm_password_reset,
    user_log_in,
    user_log_out,
    user_request_password_reset,
    user_sign_up,
)
from projectify.user.services.internal import Token


# Django view
def log_out(request: HttpRequest) -> HttpResponse:
    """Log the user out. Need to be logged in first."""
    user = request.user
    if not user.is_anonymous:
        user_log_out(request=request)
    return redirect("/")


class SignUpForm(forms.Form):
    """Sign up form."""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    tos_agreed = forms.BooleanField()
    privacy_policy_agreed = forms.BooleanField()

    email.widget.attrs.update({"placeholder": _("Enter your email")})
    password.widget.attrs.update({"placeholder": _("Enter your password")})


# No authentication required
@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="10/h", method=UNSAFE)
def sign_up(request: HttpRequest) -> HttpResponse:
    """Sign the user up."""
    validators = password_validators_help_texts()

    if request.method == "GET":
        form = SignUpForm()
        context = {"form": form, "validators": validators}
        return render(request, "user/sign_up.html", context=context)

    # XXX
    # Originally, I wanted 4/h but there's a weird off-by-one issue here
    # See the comment below as well.
    limit = get_usage(
        request,
        group="projectify.user.views.auth.sign_up",
        key="ip",
        rate="3/h",
        increment=False,
    )

    form = SignUpForm(request.POST)

    # Rate limit and show appropraite error message
    if limit and limit["should_limit"]:
        context = {"form": form, "validators": validators}
        form.add_error(
            field=None, error=_("Too many sign up attempts. Slow down.")
        )
        return render(
            request, "user/sign_up.html", context=context, status=429
        )

    if not form.is_valid():
        context = {"form": form, "validators": validators}
        return render(
            request, "user/sign_up.html", context=context, status=400
        )
    data = form.cleaned_data

    try:
        user_sign_up(
            email=data["email"],
            password=data["password"],
            tos_agreed=data["tos_agreed"],
            privacy_policy_agreed=data["privacy_policy_agreed"],
        )
    except ValidationError as error:
        populate_form_with_drf_errors(form, error)
        context = {"form": form, "validators": validators}
        return render(
            request, "user/sign_up.html", context=context, status=400
        )

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


def email_confirmation_link_sent(request: HttpRequest) -> HttpResponse:
    """Confirm sign up and tell user about confirmation email."""
    return render(request, "user/email_confirmation_link_sent.html")


def email_confirm(
    request: HttpRequest, email: str, token: str
) -> HttpResponse:
    """Confirm a new user's email address."""
    token = Token(token)

    try:
        user_confirm_email(email=email, token=token)
        context = {}
    except ValidationError as e:
        match e.detail:
            case {"email": email_error}:
                token_error = None
            case {"token": token_error}:
                email_error = None
            case _:
                raise ValueError(
                    "Don't know how to handle ValidationError of type "
                    f"{type(e)}"
                ) from e
        context = {
            "email_error": email_error,
            "token_error": token_error,
        }
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
        # Refactor the anchor tag creation and make a Django template tag
        self.fields[
            "password"
        ].help_text = '<a class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base" href="{href}">{text}</a>'.format(
            href=reverse_lazy("users:request-password-reset"),
            text=_("Forgot password"),
        )


@require_http_methods(["GET", "POST"])
@ratelimit(key="ip", rate="5/m", method=UNSAFE)
def log_in(request: HttpRequest) -> HttpResponse:
    """Log the user in."""
    FAILED_GROUP = "projectify.user.views.auth.log_in.fail"
    FAILED_KEY = "post:email"
    FAILED_RATE = "4/h"
    if request.method == "GET":
        form = LogInForm()
        context = {"form": form}
        return render(request, "user/log_in.html", context=context)

    limit = get_usage(
        request,
        group=FAILED_GROUP,
        key=FAILED_KEY,
        rate=FAILED_RATE,
        increment=False,
    )

    form = LogInForm(request.POST)
    context = {"form": form}

    if limit and limit["should_limit"]:
        context = {"form": form}
        form.add_error(
            field=None, error=_("Too many log in attempts. Slow down.")
        )
        return render(request, "user/log_in.html", context=context, status=429)

    if not form.is_valid():
        return render(request, "user/log_in.html", context=context, status=400)

    try:
        user_log_in(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            request=request,
        )
    except ValidationError as error:
        populate_form_with_drf_errors(form, error)
        context = {"form": form}
        get_usage(
            request,
            group=FAILED_GROUP,
            key=FAILED_KEY,
            rate=FAILED_RATE,
            increment=True,
        )
        return render(request, "user/log_in.html", context=context, status=400)

    next = request.GET.get("next", reverse("dashboard:dashboard"))
    return redirect(next)


class PasswordResetRequestForm(forms.Form):
    """Form for requesting a password reset."""

    email = forms.EmailField()
    email.widget.attrs.update({"placeholder": _("Enter your email")})


@require_http_methods(["GET", "POST"])
@ratelimit(key="post:email", rate="5/h")
@ratelimit(key="ip", rate="5/h")
def password_reset_request(request: HttpRequest) -> HttpResponse:
    """Request a password reset."""
    if request.method == "GET":
        form = PasswordResetRequestForm()
        context = {"form": form}
        return render(
            request, "user/password_reset_request.html", context=context
        )

    form = PasswordResetRequestForm(request.POST)
    if not form.is_valid():
        context = {"form": form}
        return render(
            request,
            "user/password_reset_request.html",
            context=context,
            status=400,
        )

    try:
        user_request_password_reset(email=form.cleaned_data["email"])
    except ValidationError as error:
        populate_form_with_drf_errors(form, error)
        context = {"form": form}
        return render(
            request,
            "user/password_reset_request.html",
            context=context,
            status=400,
        )

    return redirect("users:requested-password-reset")


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
    # TODO add validators

    if request.method == "GET":
        form = PasswordResetConfirmForm()
        context = {"form": form}
        return render(
            request, "user/password_reset_confirm.html", context=context
        )

    form = PasswordResetConfirmForm(request.POST)
    if not form.is_valid():
        context = {"form": form}
        return render(
            request,
            "user/password_reset_confirm.html",
            context=context,
            status=400,
        )

    try:
        user_confirm_password_reset(
            email=email,
            token=token,
            new_password=form.cleaned_data["new_password"],
            new_password_confirm=form.cleaned_data["new_password_confirm"],
        )
    except ValidationError as error:
        populate_form_with_drf_errors(form, error)
        context = {"form": form}
        return render(
            request,
            "user/password_reset_confirm.html",
            context=context,
            status=400,
        )

    return redirect("users:reset-password")


def password_reset(request: HttpRequest) -> HttpResponse:
    """Notify the user that they have changed their password."""
    return render(request, "user/password_reset.html")
