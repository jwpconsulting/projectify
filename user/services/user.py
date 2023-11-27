"""User model services in user app."""
from typing import Optional

from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

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
    # TODO raise ValidationError on DoesNotExist
    user = User.objects.get_by_natural_key(email)
    # TODO raise ValidationError on wrong token
    if not user.check_email_confirmation_token(token):
        return None
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
        # TODO here we should give a proper error
        return None
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
        # TODO raise a ValidationError here
        return None
    logout(request)


def user_request_password_reset(
    *,
    # Should this be taking in a user object instead?
    email: str,
) -> None:
    """Send a password reset email to a user, given their email address."""
    # TODO raise ValidationError here on DoesNotExist
    user = User.objects.get_by_natural_key(email)
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
    # TODO raise ValidationError here on DoesNotExist
    user = User.objects.get_by_natural_key(email)
    if not user.check_password_reset_token(token):
        # TODO raise a ValidationError here instead
        return None
    user.set_password(new_password)
    user.save()
    # XXX consider if returning a user is necessary here
    return user
