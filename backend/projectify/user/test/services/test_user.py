# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test user services."""

import re

from django.core.files.uploadedfile import SimpleUploadedFile

import pytest
from faker import Faker
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from projectify.user.services.internal import Token, user_make_token
from pytest_types import Mailbox

from ...models import User
from ...services.user import (
    user_change_password,
    user_confirm_email_address_update,
    user_request_email_address_update,
    user_update,
)

pytestmark = pytest.mark.django_db


def test_user_update(
    user: User, faker: Faker, uploaded_file: SimpleUploadedFile
) -> None:
    """Test updating a user."""
    new_name = faker.name()
    user_update(
        who=user,
        user=user,
        preferred_name=new_name,
        profile_picture=uploaded_file,
    )
    user.refresh_from_db()
    assert user.preferred_name == new_name
    assert "profile_picture/test_" in user.profile_picture.path


def test_user_change_password_weak_password(user: User, password: str) -> None:
    """Test changing password with weak password."""
    with pytest.raises(ValidationError):
        user_change_password(
            user=user,
            current_password=password,
            new_password="asd123",
        )

    user.refresh_from_db()
    assert user.check_password("asd123") is False
    assert user.check_password(password) is True


def test_user_change_password(
    user: User, password: str, mailoutbox: Mailbox
) -> None:
    """
    Test changing a user's password. Check that notification email goes out.

    Tests with a reaaaalllyyyy long password.
    """
    new_password = "hello-123" * 100
    # First we give in the wrong old password
    with pytest.raises(serializers.ValidationError):
        user_change_password(
            user=user, current_password="wrongpw123", new_password=new_password
        )

    user.refresh_from_db()
    assert user.check_password(new_password) is False
    assert len(mailoutbox) == 0

    # Then try with correct current password
    user_change_password(
        user=user, current_password=password, new_password=new_password
    )
    user.refresh_from_db()
    assert user.check_password(new_password) is True
    (mail,) = mailoutbox
    assert "password has been changed" in mail.body


def test_user_email_update_complete(
    user: User,
    password: str,
    faker: Faker,
    mailoutbox: Mailbox,
) -> None:
    """
    Test requesting for user's email address to be updated.

    Scenarios we want to test:
    1) Wrong password will throw during request
    2) Wrong token will throw during confirm
    3) Other kind token will throw during confirm
    4) Same previously valid token will throw if try to confirm again
    """
    old_email = user.email
    new_email = faker.email()

    # Try with wrong password
    with pytest.raises(serializers.ValidationError):
        user_request_email_address_update(
            user=user,
            new_email=new_email,
            password="blabla",
        )
    assert len(mailoutbox) == 0

    # Request with correct password
    user_request_email_address_update(
        user=user,
        new_email=new_email,
        password=password,
    )

    # Assert we get an email
    assert len(mailoutbox) == 1
    body = mailoutbox[0].body
    match = re.search(r"update-email-address/confirm/(.+)\n", body)
    assert match
    token = Token(match.group(1))

    # Completely invalid token
    with pytest.raises(serializers.ValidationError):
        user_confirm_email_address_update(
            user=user, confirmation_token=Token("wrong-token")
        )
    user.refresh_from_db()
    assert user.email == old_email

    # Wrong kind of token
    wrong_kind_token = user_make_token(user=user, kind="reset_password")
    with pytest.raises(serializers.ValidationError):
        user_confirm_email_address_update(
            user=user, confirmation_token=wrong_kind_token
        )
    user.refresh_from_db()
    assert user.email == old_email

    # Correct token
    user_confirm_email_address_update(user=user, confirmation_token=token)
    user.refresh_from_db()
    assert user.email == new_email

    # Can't do it twice
    with pytest.raises(serializers.ValidationError):
        user_confirm_email_address_update(user=user, confirmation_token=token)

    # Ensure second email is sent out
    assert len(mailoutbox) == 2
    body = mailoutbox[1].body
    assert "has been updated" in body
    assert match
    token = Token(match.group(1))
