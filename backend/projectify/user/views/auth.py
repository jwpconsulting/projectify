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
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from django_ratelimit.core import UNSAFE, get_usage
from django_ratelimit.decorators import ratelimit
from rest_framework import serializers, views
from rest_framework.exceptions import Throttled, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.forms import populate_form_with_drf_errors
from projectify.lib.schema import extend_schema
from projectify.user.serializers import (
    AnonymousUserSerializer,
    LoggedInUserSerializer,
)
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
    return redirect("users-django:sent-email-confirmation-link")


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
            href=reverse_lazy("users-django:request-password-reset"),
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

    return redirect("users-django:requested-password-reset")


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

    return redirect("users-django:reset-password")


def password_reset(request: HttpRequest) -> HttpResponse:
    """Notify the user that they have changed their password."""
    return render(request, "user/password_reset.html")


# DRF Views
class LogOut(views.APIView):
    """Log a user out."""

    @extend_schema(request=None, responses={200: AnonymousUserSerializer})
    def post(self, request: Request) -> Response:
        """Handle POST."""
        user_log_out(request=request)
        serializer = AnonymousUserSerializer(
            instance={"kind": "unauthenticated"}
        )
        return Response(status=HTTP_200_OK, data=serializer.data)


# The following views have no authentication required
class SignUp(views.APIView):
    """Sign up a user."""

    permission_classes = (AllowAny,)

    class SignUpSerializer(serializers.Serializer):
        """Take in email and password."""

        email = serializers.EmailField()
        password = serializers.CharField()
        tos_agreed = serializers.BooleanField()
        privacy_policy_agreed = serializers.BooleanField()

    @extend_schema(
        request=SignUpSerializer,
        responses={204: None, 400: DeriveSchema, 429: DeriveSchema},
    )
    @method_decorator(ratelimit(key="ip", rate="60/h"))
    def post(self, request: Request) -> Response:
        """Handle POST."""
        # See if we are throttled
        limit = get_usage(
            request,
            group="projectify.user.views.auth.SignUp.post",
            key="ip",
            rate="4/h",
            increment=False,
        )
        if limit and limit["should_limit"]:
            raise Throttled()

        serializer = self.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_sign_up(
            email=data["email"],
            password=data["password"],
            tos_agreed=data["tos_agreed"],
            privacy_policy_agreed=data["privacy_policy_agreed"],
        )

        # Increment limit only on success
        get_usage(
            request,
            group="projectify.user.views.auth.SignUp.post",
            key="ip",
            rate="4/h",
            increment=True,
        )

        return Response(status=HTTP_204_NO_CONTENT)


class ConfirmEmail(views.APIView):
    """Log a user in."""

    permission_classes = (AllowAny,)

    class ConfirmEmailSerializer(serializers.Serializer):
        """Take email and password."""

        email = serializers.EmailField()
        token = serializers.CharField()

    @extend_schema(
        request=ConfirmEmailSerializer,
        responses={204: None, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.ConfirmEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_confirm_email(
            email=data["email"],
            token=data["token"],
        )
        return Response(status=HTTP_204_NO_CONTENT)


class LogIn(views.APIView):
    """Log a user in. Return user to signify success."""

    permission_classes = (AllowAny,)

    class LogInSerializer(serializers.Serializer):
        """Take email and password."""

        email = serializers.EmailField()
        password = serializers.CharField()

    @extend_schema(
        request=LogInSerializer,
        responses={
            200: LoggedInUserSerializer,
            400: DeriveSchema,
            429: DeriveSchema,
        },
    )
    @method_decorator(
        ratelimit(
            group="projectify.user.views.auth.login.post",
            key="post:email",
            rate="60/h",
        )
    )
    @method_decorator(
        ratelimit(
            group="projectify.user.views.auth.LogIn.post",
            key="ip",
            rate="10/m",
        )
    )
    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.LogInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = user_log_in(
                email=data["email"], password=data["password"], request=request
            )
        except serializers.ValidationError as e:
            limit = get_usage(
                request,
                group="projectify.user.views.auth.LogIn.post",
                key="post:email",
                rate="5/m",
                increment=True,
            )
            if limit and limit["should_limit"]:
                raise Throttled()
            else:
                raise e
        response_serializer = LoggedInUserSerializer(instance=user)
        return Response(data=response_serializer.data, status=HTTP_200_OK)


# Reset password
class PasswordResetRequest(views.APIView):
    """
    Request password to be reset.

    Rate limited to 5 times per email per hour.
    """

    permission_classes = (AllowAny,)

    class PasswordResetRequestSerializer(serializers.Serializer):
        """Take an email address."""

        email = serializers.EmailField()

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={204: None, 400: DeriveSchema, 429: DeriveSchema},
    )
    @method_decorator(ratelimit(key="post:email", rate="5/h"))
    @method_decorator(ratelimit(key="ip", rate="5/h"))
    @method_decorator(ratelimit(key="ip", rate="1/m"))
    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_request_password_reset(email=data["email"])
        return Response(status=HTTP_204_NO_CONTENT)


class PasswordResetConfirm(views.APIView):
    """Reset a user's password."""

    permission_classes = (AllowAny,)

    class PasswordResetConfirmSerializer(serializers.Serializer):
        """Take email, token and a new password."""

        email = serializers.EmailField()
        token = serializers.CharField()
        new_password = serializers.CharField()

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={204: None, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_confirm_password_reset(
            email=data["email"],
            token=data["token"],
            new_password=data["new_password"],
        )
        return Response(status=HTTP_204_NO_CONTENT)


class PasswordPolicyRead(views.APIView):
    """Return information about password policy."""

    permission_classes = (AllowAny,)

    class PasswordPoliciesSerializer(serializers.Serializer):
        """Serialize password policies."""

        policies = serializers.ListField(child=serializers.CharField())

    @extend_schema(
        responses={
            200: PasswordPoliciesSerializer,
        },
    )
    def get(self, request: Request) -> Response:
        """Return all information about current password policy."""
        del request
        validators = password_validators_help_texts()
        serializer = self.PasswordPoliciesSerializer(
            instance={"policies": validators}
        )
        return Response(data=serializer.data, status=HTTP_200_OK)
