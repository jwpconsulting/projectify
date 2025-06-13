# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Test user emails."""

import re

from django.core.mail import EmailMessage
from django.test.client import Client

import pytest

from projectify.user.services.internal import Token, user_check_token

from ..emails import (
    UserEmailAddressUpdateEmail,
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


@pytest.mark.django_db
class TestUserEmailAddressUpdateEmail:
    """Test UserEmailAddressUpdateEmail."""

    def test_send(
        self, user: User, user_client: Client, mailoutbox: list[EmailMessage]
    ) -> None:
        """Test send."""
        new_email = "new-email@example.com"
        user.unconfirmed_email = new_email
        user.save()
        UserEmailAddressUpdateEmail(receiver=user, obj=user).send()
        assert len(mailoutbox) == 1, mailoutbox

        m = mailoutbox[0]
        assert m.to == [new_email]
        assert new_email in m.body
        match = re.search(
            r"(/user/profile/update-email-address/confirm/.+)\n", m.body
        )
        assert match, m.body
        response = user_client.get(match.group(1))
        assert response.status_code == 200, response
        user.refresh_from_db()
        assert user.email == new_email
