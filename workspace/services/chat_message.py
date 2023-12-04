"""
Chat message services.

Chat messages will not be in the initial launch.
"""
from projectify.utils import validate_perm
from user.models import User
from workspace.models.chat_message import ChatMessage
from workspace.models.task import Task
from workspace.selectors.workspace_user import (
    workspace_user_find_for_workspace,
)


# TODO this could take an author instead of who -> user is derived from author
def chat_message_create(
    *,
    who: User,
    task: Task,
    text: str,
) -> ChatMessage:
    """Create a chat message for a task."""
    validate_perm("workspace.can_create_chat_message", who, task)
    workspace_user = workspace_user_find_for_workspace(
        workspace=task.workspace,
        user=who,
    )
    return ChatMessage.objects.create(
        task=task, text=text, author=workspace_user
    )
