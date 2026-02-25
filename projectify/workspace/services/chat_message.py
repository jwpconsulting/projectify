# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
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
    return instance
