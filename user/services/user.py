"""User model services in user app."""
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
