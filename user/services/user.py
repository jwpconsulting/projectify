"""User model services in user app."""
from typing import Optional

from user.emails import UserEmailConfirmationEmail
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
    user = User.objects.get_by_natural_key(email)
    if not user.check_email_confirmation_token(token):
        return None
    user.is_active = True
    user.save()
    return user
