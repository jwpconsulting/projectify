# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test chat message services."""

import pytest
from faker import Faker

from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.chat_message import chat_message_create


@pytest.mark.django_db
def test_add_chat_message(
    task: Task,
    team_member: TeamMember,
    faker: Faker,
) -> None:
    """Test adding a chat message."""
    assert task.chatmessage_set.count() == 0
    chat_message = chat_message_create(
        who=team_member.user,
        task=task,
        text=faker.paragraph(),
    )
    assert task.chatmessage_set.count() == 1
    assert chat_message.author == team_member
