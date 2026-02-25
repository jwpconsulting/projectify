# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Test user emails."""

import re

from django.core.mail import EmailMessage
from django.test.client import Client

import pytest

from ..emails import (
    UserEmailAddressUpdateEmail,
    UserEmailConfirmationEmail,
    UserPasswordResetEmail,
)
from ..models import User


@pytest.mark.django_db
class TestUserEmailConfirmationEmail:
    """Test UserEmailConfirmationEmail."""

    def test_send(
        self, client: Client, user: User, mailoutbox: list[EmailMessage]
    ) -> None:
        """Test send."""
        user.is_active = False
        user.email = "space@example.com"
        user.save()
        assert not user.is_active
        mail = UserEmailConfirmationEmail(receiver=user, obj=user)
        mail.send()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert user.email in m.body
        match = re.search("(/user/confirm-email/.+/.+)\n", m.body)
        assert match
        response = client.get(match.group(1))
        user.refresh_from_db()
        assert response.status_code == 200
        assert user.is_active


@pytest.mark.django_db
class TestUserPasswordResetEmail:
    """Test UserPasswordResetEmail."""

    def test_send(
        self, client: Client, user: User, mailoutbox: list[EmailMessage]
    ) -> None:
        """Test send."""
        mail = UserPasswordResetEmail(receiver=user, obj=user)
        mail.send()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert user.email in m.body
        match = re.search("(/user/confirm-password-reset/.+/.+)\n", m.body)
        assert match, m.body
        response = client.get(match.group(1))
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserEmailAddressUpdateEmail:
    """Test UserEmailAddressUpdateEmail."""

    def test_send(
        self, user: User, user_client: Client, mailoutbox: list[EmailMessage]
    ) -> None:
        """
        Test sending this email.

        This test reimplements some of the test code in
        `test_user_email_update_complete` in projectify/user/test/services/test_user.py.
        """
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
        assert response.status_code == 302, response
        user.refresh_from_db()
        assert user.email == new_email
