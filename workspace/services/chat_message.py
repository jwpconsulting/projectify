"""
Chat message services.

Chat messages will not be in the initial launch.
"""
from projectify.utils import validate_perm
from user.models import User
from workspace.models.chat_message import ChatMessage
from workspace.models.task import Task
from workspace.models.workspace_user import WorkspaceUser


def chat_message_create(
    *,
    who: User,
    task: Task,
    text: str,
) -> ChatMessage:
    """Create a chat message for a task."""
    validate_perm("workspace.can_create_chat_message", who, task)
    workspace_user = WorkspaceUser.objects.get_by_workspace_and_user(
        task.workspace,
        who,
    )
    return ChatMessage.objects.create(
        task=task, text=text, author=workspace_user
    )
