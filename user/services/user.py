"""User model services in user app."""
from typing import Optional

from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from user.emails import UserEmailConfirmationEmail, UserPasswordResetEmail
from user.models import User


def user_sign_up(
    *,
    email: str,
    password: str,
) -> User:
    """Sign up a user."""
    user = User.objects.create_user(
        email=email,
        password=password,
    )
    mail = UserEmailConfirmationEmail(user)
    mail.send()
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
