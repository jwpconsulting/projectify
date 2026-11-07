# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022 JWP Consulting GK
"""Test premail emails."""

import pytest

from projectify.user.models import User
from pytest_types import Mailbox

from ..emails import SampleEmail


@pytest.mark.django_db
class TestSampleEmail:
    """Test SampleEmail."""

    def test_send(self, user: User, mailoutbox: Mailbox) -> None:
        """Test send."""
        mail = SampleEmail(receiver=user, obj=user)
        mail.send()
        assert len(mailoutbox) == 1
