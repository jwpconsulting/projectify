"""User model services in user app."""
import logging
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from user.emails import UserEmailConfirmationEmail, UserPasswordResetEmail
from user.models import User, UserManager
from user.selectors.user import user_find_by_email
from user.services.user_invite import user_invite_redeem_many

logger = logging.getLogger(__name__)


# Create
def _user_create(
    email: str,
    password: Optional[str],
    is_staff: bool,
    is_superuser: bool,
    is_active: bool,
) -> "User":
    """Create and save a user with the given email, and password."""
    email = UserManager.normalize_email(email)
    user = User(
        email=email,
        is_staff=is_staff,
        is_superuser=is_superuser,
        is_active=is_active,
    )
    user.password = make_password(password)
    # XXX self._db needed? user.save(using=self._db)
    user.save()
    user_invite_redeem_many(user=user)
    return user


def user_create(
    # TODO add initial *
    email: str,
    password: Optional[str] = None,
) -> "User":
    """Create a normal user."""
    return _user_create(
        email,
        password,
        is_staff=False,
        is_superuser=False,
        is_active=False,
    )


def user_create_superuser(
    # TODO add initial *
    email: str,
    password: Optional[str] = None,
) -> "User":
    """Create a superuser."""
    return _user_create(
        email,
        password,
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )


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
    # Check if user exists
    if user_find_by_email(email=email) is not None:
        raise serializers.ValidationError(
            {
                "email": _(
                    "A user with this email address is already registered"
                )
            }
        )
    # Here we should validate the password with Django's validation criteria
    user = user_create(
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
    user = user_find_by_email(email=email)
    if user is None:
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
    user = authenticate(request, username=email, password=password)
    if user is None:
        maybe_user = user_find_by_email(email=email)
        if maybe_user is None:
            logger.warning("Could not find a user for %s", email)
            raise serializers.ValidationError(
                {"email": _("No user could be found for this email address")}
            )
        if not maybe_user.is_active:
            logger.warning(
                "Tried to log in for inactive user with email %s", email
            )
            raise serializers.ValidationError(
                {
                    "email": _(
                        "This email address has not been confirmed. "
                        "Please check your email inbox for a confirmation email or contact our support if you need further help."
                    )
                }
            )
        logger.warning(
            "User with email %s found but authentication failed", email
        )
        raise serializers.ValidationError(
            {"password": _("No user could be found for this email address")}
        )
    login(request, user)
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
    user = user_find_by_email(email=email)
    if user is None:
        raise serializers.ValidationError(
            {"email": _("No user could be found for this email")}
        )
    password_reset_email = UserPasswordResetEmail(user)
    password_reset_email.send()


@transaction.atomic
def user_confirm_password_reset(
    *,
    email: str,
    token: str,
    new_password: str,
    # TODO don't return anything here
) -> Optional[User]:
    """Reset a user's password given a new password and a reset token."""
    user = user_find_by_email(email=email)
    if user is None:
        logger.warning(
            "Could not find email %s when attempting to reset a password",
            email,
        )
        raise serializers.ValidationError(
            {"email": _("This email is not recognized")}
        )
    if not user.check_password_reset_token(token):
        logger.warning("Could not match a reset token to email %s", email)
        raise serializers.ValidationError(
            {"token": _("This token is invalid")}
        )
    user.set_password(new_password)
    user.save()
    logger.info("Reset password for user with email %s", email)
    # XXX consider if returning a user is necessary here
    return user
