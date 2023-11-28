"""Test chat message services."""
import pytest
from faker import Faker

from workspace.models.task import Task
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.chat_message import chat_message_create


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
