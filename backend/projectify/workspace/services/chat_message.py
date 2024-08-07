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
"""
Chat message services.

Chat messages will not be in the initial launch.
"""

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.chat_message import ChatMessage
from projectify.workspace.models.task import Task
from projectify.workspace.selectors.team_member import (
    team_member_find_for_workspace,
)
from projectify.workspace.services.signals import send_change_signal


# TODO this could take an author instead of who -> user is derived from author
def chat_message_create(
    *,
    who: User,
    task: Task,
    text: str,
) -> ChatMessage:
    """Create a chat message for a task."""
    validate_perm("workspace.create_chat_message", who, task.workspace)
    team_member = team_member_find_for_workspace(
        workspace=task.workspace,
        user=who,
    )
    instance = ChatMessage.objects.create(
        task=task, text=text, author=team_member
    )
    send_change_signal("changed", task)
    return instance
