# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022 JWP Consulting GK
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
"""Test premail emails."""
import pytest

from projectify.user.models.user import User
from pytest_types import Mailbox

from ..emails import (
    SampleEmail,
)


@pytest.mark.django_db
class TestSampleEmail:
    """Test SampleEmail."""

    def test_send(self, user: User, mailoutbox: Mailbox) -> None:
        """Test send."""
        mail = SampleEmail(receiver=user, obj=user)
        mail.send()
        assert len(mailoutbox) == 1
