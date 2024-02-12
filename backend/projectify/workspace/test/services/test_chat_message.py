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
"""Test chat message services."""
import pytest
from faker import Faker

from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.chat_message import chat_message_create


@pytest.mark.django_db
def test_add_chat_message(
    task: Task,
    workspace_user: WorkspaceUser,
    faker: Faker,
) -> None:
    """Test adding a chat message."""
    assert task.chatmessage_set.count() == 0
    chat_message = chat_message_create(
        who=workspace_user.user,
        task=task,
        text=faker.paragraph(),
    )
    assert task.chatmessage_set.count() == 1
    assert chat_message.author == workspace_user
