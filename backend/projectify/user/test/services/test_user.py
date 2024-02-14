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
"""Test user services."""

import pytest
from faker import Faker
from rest_framework import serializers

from pytest_types import Mailbox

from ...models import User
from ...services.user import user_change_password, user_update

pytestmark = pytest.mark.django_db


def test_user_update(user: User, faker: Faker) -> None:
    """Test updating a user."""
    new_name = faker.name()
    user_update(who=user, user=user, preferred_name=new_name)
    user.refresh_from_db()
    assert user.preferred_name == new_name


def test_user_change_password(
    user: User, password: str, faker: Faker, mailoutbox: Mailbox
) -> None:
    """Test changing a user's password. Check that notification email goes out."""
    new_password = "hello-123"
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
