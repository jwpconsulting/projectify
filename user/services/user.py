"""User model services in user app."""
from typing import Optional

from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from user.emails import UserEmailConfirmationEmail, UserPasswordResetEmail
from user.models import User


# Update
def user_update(
    *,
    who: User,
    user: User,
    full_name: Optional[str],
) -> User:
    """Update a user."""
    if not who == user:
        raise PermissionDenied("User can only update own user")
    user.full_name = full_name
    user.save()
    return user


# RPC style
def user_sign_up(
    *,
    email: str,
    password: str,
) -> User:
    """Sign up a user."""
    # Here we should validate the password with Django's validation criteria
    user = User.objects.create_user(
        email=email,
        password=password,
    )
    mail = UserEmailConfirmationEmail(user)
    mail.send()
    # TODO do not return User here
    return user


def user_confirm_email(
    *,
    email: str,
    token: str,
) -> Optional[User]:
    """Confirm a user's email, return User on success."""
    try:
        user = User.objects.get_by_natural_key(email)
    except User.DoesNotExist:
        raise serializers.ValidationError(
            {"email": _("No user could be found for this email address")}
        )
    if not user.check_email_confirmation_token(token):
        raise serializers.ValidationError(
            {"token": _("This email confirmation token is invalid")}
        )
    user.is_active = True
    user.save()
    # TODO do not return User here
    return user


def user_log_in(
    *,
    email: str,
    password: str,
    request: HttpRequest,
) -> Optional[User]:
    """Log a user in, return cookies."""
    user = ModelBackend().authenticate(
        request,
        username=email,
        password=password,
    )
    if user is None:
        raise serializers.ValidationError(
            _("No user could be found for these credentials")
        )
    login(
        request,
        user,
        # The backend is hardcoded here ... hopefully that won't be an issue
        backend="django.contrib.auth.backends.ModelBackend",
    )
    if not isinstance(user, User):
        raise ValueError("User is not User, why?")
    # XXX consider if returning a user is necessary here
    return user


def user_log_out(
    *,
    request: HttpRequest,
) -> None:
    """Log a user out, update cookies."""
    user = request.user
    if user.is_anonymous:
        raise serializers.ValidationError(_("There is no logged in user"))
    logout(request)


def user_request_password_reset(
    *,
    # Should this be taking in a user object instead?
    email: str,
) -> None:
    """Send a password reset email to a user, given their email address."""
    try:
        user = User.objects.get_by_natural_key(email)
    except User.DoesNotExist:
        raise serializers.ValidationError(
            {"email": _("No user could be found for this email")}
        )
    password_reset_email = UserPasswordResetEmail(user)
    password_reset_email.send()


def user_confirm_password_reset(
    *,
    email: str,
    token: str,
    new_password: str,
    # TODO don't return anything here
) -> Optional[User]:
    """Reset a user's password given a new password and a reset token."""
    try:
        user = User.objects.get_by_natural_key(email)
    except User.DoesNotExist:
        raise serializers.ValidationError(
            {"email": _("This email is not recognized")}
        )
    if not user.check_password_reset_token(token):
        raise serializers.ValidationError(
            {"token": _("This token is invalid")}
        )
    user.set_password(new_password)
    user.save()
    # XXX consider if returning a user is necessary here
    return user
