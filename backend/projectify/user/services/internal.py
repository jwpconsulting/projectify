# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Internal services, not user facing."""
from datetime import datetime
from typing import Literal, NewType, Optional

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from projectify.user.models.user import User
from projectify.user.services.user_invite import user_invite_redeem_many


def _user_create(
    email: str,
    password: Optional[str],
    is_staff: bool,
    is_superuser: bool,
    is_active: bool,
    tos_agreed: Optional[datetime] = None,
    privacy_policy_agreed: Optional[datetime] = None,
) -> User:
    """Create and save a user with the given email, and password."""
    email = User.objects.normalize_email(email)
    user = User(
        email=email,
        is_staff=is_staff,
        is_superuser=is_superuser,
        is_active=is_active,
        tos_agreed=tos_agreed,
        privacy_policy_agreed=privacy_policy_agreed,
    )
    # TODO cann this be user.set_password(password) ?
    user.password = make_password(password)
    # XXX self._db needed? user.save(using=self._db)
    user.save()
    user_invite_redeem_many(user=user)
    return user


def user_create(
    *,
    email: str,
    password: Optional[str] = None,
    tos_agreed: Optional[datetime] = None,
    privacy_policy_agreed: Optional[datetime] = None,
) -> User:
    """Create a normal user."""
    return _user_create(
        email,
        password,
        is_staff=False,
        is_superuser=False,
        is_active=False,
        tos_agreed=tos_agreed,
        privacy_policy_agreed=privacy_policy_agreed,
    )


def user_create_superuser(
    *,
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


TokenKind = Literal[
    "confirm_email_address", "reset_password", "update_email_address"
]
Token = NewType("Token", str)


def user_make_token(*, user: User, kind: TokenKind) -> Token:
    """
    Return a salted token of 'kind' for a user.

    This is guaranteed to unique for a given user state and token kind.

    A user state is derived by Django's PasswordResetTokenGenerator using the
    user's primary key, email and "some user state" that will change if the
    action is performed for which this token is generated.

    For password reset:
    1. user requests password reset
    2. changes password using token
    3. user state changes
    4. previous token becomes invalid (since password is different)

    For email confirm:
    1. user automatically receives email confirm token
    2. user confirms their email using the link in the email
    3. state doesn't change? But! Not an issue, the user should feel free to
    confirm their email address as often as they want to. It's idempotent, so
    to say. And then:
    4. user changes their email address
    5. the previously generated token will not work anymore

    For email change:
    1. user requests their email address to be changed
    2. token is generated (using the old email address)
    3. user confirms the new email address
    4. token is invalidated, they can't use it again.

    In a way, email confirm and email change are about confirming a new email
    address. Since the email confirm is entwined into the business logic of
    confirming and onboarding users, we would like to keep these two separate.

    As an advantage over the previous tokens that we generated, the Django
    builtin tokens have a timelimit configured using
    settings.PASSWORD_RESET_TIMEOUT

    The way we made tokens before added the risk of collision, especially for
    email addresses. Now, since we use more user state to generate tokens,
    this risk is addresses sufficiently (for example, user.pk is sure to be
    different between users)
    """
    generator = PasswordResetTokenGenerator()
    generator.key_salt = kind
    token = generator.make_token(user)
    return Token(token)


def user_check_token(*, user: User, kind: TokenKind, token: Token) -> bool:
    """
    Check if a token passed to us is correct.

    Use Django's PasswordResetTokenGenerator salted with TokenKind.
    """
    generator = PasswordResetTokenGenerator()
    generator.key_salt = kind
    return generator.check_token(user, token)
