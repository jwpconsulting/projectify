# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Test user emails."""

import re

from django.core.mail import EmailMessage

import pytest

from projectify.user.services.internal import (
    Token,
    user_check_token,
)

from ..emails import (
    UserEmailConfirmationEmail,
    UserPasswordResetEmail,
)
from ..models import User


@pytest.mark.django_db
class TestUserEmailConfirmationEmail:
    """Test UserEmailConfirmationEmail."""

    def test_send(self, user: User, mailoutbox: list[EmailMessage]) -> None:
        """Test send."""
        user.email = "space@example.com"
        user.save()
        mail = UserEmailConfirmationEmail(receiver=user, obj=user)
        mail.send()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert "space%40example.com" in m.body
        match = re.search("/user/confirm-email/.+/(.+)\n", m.body)
        assert match
        token = Token(match.group(1))
        assert user_check_token(
            token=token, user=user, kind="confirm_email_address"
        )


@pytest.mark.django_db
class TestUserPasswordResetEmail:
    """Test UserPasswordResetEmail."""

    def test_send(self, user: User, mailoutbox: list[EmailMessage]) -> None:
        """Test send."""
        mail = UserPasswordResetEmail(receiver=user, obj=user)
        mail.send()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        match = re.search("/user/confirm-password-reset/.+/(.+)\n", m.body)
        assert match
        token = Token(match.group(1))
        assert user_check_token(token=token, user=user, kind="reset_password")
