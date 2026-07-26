# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Test user app internal services."""

from datetime import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator

import pytest

from projectify.settings.base import Base

from ...models import User
from ...services.internal import (
    Token,
    TokenKind,
    user_check_token,
    user_create,
    user_create_superuser,
    user_make_token,
)

pytestmark = pytest.mark.django_db


def test_user_create() -> None:
    """Test creating a normal user."""
    u = user_create(email="hello@localhost")
    assert u.is_active is False


def test_user_create_superuser() -> None:
    """Test creating a superuser. A superuser should be active."""
    u = user_create_superuser(email="hello@localhost")
    assert u.is_active is True


@pytest.fixture
def deterministic_user() -> User:
    """Return user with predictable fields for token fn checking."""
    return User(pk=1, last_login=None, email="hello@example", password="abc")


def now(_self: object) -> datetime:
    """Return fixed datetime for PasswordResetTokenGenerator."""
    return datetime(2024, 2, 15)


tokens: list[tuple[TokenKind, Token]] = [
    (
        "confirm_email_address",
        Token("c2ew00-a4662d1b9eaf0ed73d8ea4595b57fdf5"),
    ),
    ("reset_password", Token("c2ew00-8c001f3e5576f8df15f416d5a93ba55b")),
    ("update_email_address", Token("c2ew00-9991c260d5933cbd003f7655f775a2a6")),
]


@pytest.fixture(autouse=True)
def deterministic_token_result(
    settings: Base, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Make sure test cases get the same token every time."""
    settings.SECRET_KEY = "test"
    monkeypatch.setattr(PasswordResetTokenGenerator, "_now", now)


@pytest.mark.parametrize("kind,token", tokens)
def test_user_make_token(
    deterministic_user: User, kind: TokenKind, token: Token
) -> None:
    """Test token making."""
    assert user_make_token(user=deterministic_user, kind=kind) == token


@pytest.mark.parametrize(
    "kind", ["confirm_email_address", "reset_password", "update_email_address"]
)
def test_user_make_token_with_unconfirmed_email(
    deterministic_user: User, kind: TokenKind
) -> None:
    """Test token making when unconfirmed_email changes."""
    token1 = user_make_token(user=deterministic_user, kind=kind)
    deterministic_user.unconfirmed_email = "abc@example.com"
    token2 = user_make_token(user=deterministic_user, kind=kind)
    assert token1 != token2
    # Make sure we can repeat this
    token3 = user_make_token(user=deterministic_user, kind=kind)
    assert token2 == token3


@pytest.mark.parametrize("kind,token", tokens)
def test_user_check_token(
    deterministic_user: User, kind: TokenKind, token: Token
) -> None:
    """Test token checking."""
    assert (
        user_check_token(user=deterministic_user, kind=kind, token=token)
        is True
    )
    # We substring the token and test that it won't validate
    wrong_token = Token(token[:-1])
    assert (
        user_check_token(user=deterministic_user, kind=kind, token=wrong_token)
        is False
    )
