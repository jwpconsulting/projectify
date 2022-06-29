"""Consumer tests."""
import pytest
from channels.db import (
    database_sync_to_async,
)
from channels.testing import (
    WebsocketCommunicator,
)

from projectify.asgi import (
    websocket_application,
)
from user.factory import (
    UserFactory,
)

from .. import (
    factory,
)


@database_sync_to_async
def create_user():
    """Create a user."""
    return UserFactory()


@database_sync_to_async
def create_workspace():
    """Create workspace."""
    return factory.WorkspaceFactory()


@database_sync_to_async
def create_workspace_user(workspace, user):
    """Create workspace user."""
    return factory.WorkspaceUserFactory(workspace=workspace, user=user)


@database_sync_to_async
def create_workspace_board(workspace):
    """Create workspace board."""
    return factory.WorkspaceBoardFactory(workspace=workspace)


@database_sync_to_async
def create_workspace_board_section(workspace_board):
    """Create workspace board section."""
    return factory.WorkspaceBoardSectionFactory(
        workspace_board=workspace_board,
    )


@database_sync_to_async
def create_task(workspace_board_section, assignee_workspace_user):
    """Create task."""
    return factory.TaskFactory(
        workspace_board_section=workspace_board_section,
        assignee_workspace_user=assignee_workspace_user,
    )


@database_sync_to_async
def create_label(workspace):
    """Create a label."""
    return factory.LabelFactory(workspace=workspace)


@database_sync_to_async
def add_label(label, task):
    """Add a label to a task."""
    task.add_label(label)


@database_sync_to_async
def remove_label(label, task):
    """Remove a label from a task."""
    task.remove_label(label)


@database_sync_to_async
def create_sub_task(task):
    """Create sub task."""
    return factory.SubTaskFactory(task=task)


@database_sync_to_async
def create_chat_message(task, user):
    """Create chat message."""
    return factory.ChatMessageFactory(task=task, author=user)


@database_sync_to_async
def save_model_instance(model_instance):
    """Save model instance."""
    model_instance.save()


@database_sync_to_async
def delete_model_instance(model_instance):
    """Delete model instance."""
    model_instance.delete()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestWorkspaceConsumer:
    """Test WorkspaceConsumer."""

    async def test_workspace_saved_or_deleted(self):
        """Test signal firing on workspace change."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        resource = f"ws/workspace/{workspace.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(workspace)
        message = await communicator.receive_json_from()
        assert message == str(workspace.uuid)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)
        message = await communicator.receive_json_from()
        assert message == str(workspace.uuid)
        await communicator.disconnect()

    async def test_label_saved_or_deleted(self):
        """Test signal firing on workspace change."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        label = await create_label(workspace)
        resource = f"ws/workspace/{workspace.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(label)
        message = await communicator.receive_json_from()
        assert message == str(workspace.uuid)
        await delete_model_instance(label)
        message = await communicator.receive_json_from()
        assert message == str(workspace.uuid)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)
        await communicator.disconnect()

    async def test_workspace_user_saved_or_deleted(self):
        """Test signal firing on workspace user save or delete."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        resource = f"ws/workspace/{workspace.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(workspace_user)
        message = await communicator.receive_json_from()
        assert message == str(workspace.uuid)
        await delete_model_instance(workspace_user)
        message = await communicator.receive_json_from()
        assert message == str(workspace.uuid)
        await communicator.disconnect()
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_workspace_board_saved_or_deleted(self):
        """Test signal firing on workspace board change."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_board = await create_workspace_board(workspace)
        workspace_user = await create_workspace_user(workspace, user)
        resource = f"ws/workspace/{workspace.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(workspace_board)
        message = await communicator.receive_json_from()
        assert message == str(workspace.uuid)
        await delete_model_instance(workspace_board)
        message = await communicator.receive_json_from()
        assert message == str(workspace.uuid)
        await communicator.disconnect()
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)


@pytest.mark.django_db
@pytest.mark.asyncio
class TestWorkspaceBoardConsumer:
    """Test WorkspaceBoardConsumer."""

    async def test_workspace_board_saved_or_deleted(self):
        """Test signal firing on workspace board change."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_board = await create_workspace_board(workspace)
        workspace_user = await create_workspace_user(workspace, user)
        resource = f"ws/workspace-board/{workspace_board.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(workspace_board)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await delete_model_instance(workspace_board)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await communicator.disconnect()
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_workspace_board_section_saved_or_deleted(self):
        """Test signal firing on workspace board section change."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        workspace_user = await create_workspace_user(workspace, user)
        resource = f"ws/workspace-board/{workspace_board.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(workspace_board_section)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await delete_model_instance(workspace_board_section)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await communicator.disconnect()
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_task_saved_or_deleted(self):
        """Test signal firing on task change."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        workspace_user = await create_workspace_user(workspace, user)
        task = await create_task(workspace_board_section, workspace_user)
        resource = f"ws/workspace-board/{workspace_board.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(task)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await delete_model_instance(task)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_label_added_or_removed(self):
        """Test workspace board update on task label add or remove."""
        user = await create_user()
        workspace = await create_workspace()
        label = await create_label(workspace)
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        workspace_user = await create_workspace_user(workspace, user)
        task = await create_task(workspace_board_section, workspace_user)
        resource = f"ws/workspace-board/{workspace_board.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await add_label(label, task)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await remove_label(label, task)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(label)
        await delete_model_instance(workspace)

    async def test_sub_task_saved_or_deleted(self):
        """Test signal firing on sub task change."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        workspace_user = await create_workspace_user(workspace, user)
        task = await create_task(workspace_board_section, workspace_user)
        sub_task = await create_sub_task(task)
        resource = f"ws/workspace-board/{workspace_board.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(sub_task)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await delete_model_instance(sub_task)
        message = await communicator.receive_json_from()
        assert message == str(workspace_board.uuid)
        await communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)


@pytest.mark.django_db
@pytest.mark.asyncio
class TestTaskConsumer:
    """Test TaskConsumer."""

    async def test_task_saved_or_deleted(self):
        """Assert event is fired when task is saved or deleted."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        task = await create_task(workspace_board_section, workspace_user)
        resource = f"ws/task/{task.uuid}/"
        communicator = WebsocketCommunicator(websocket_application, resource)
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(task)
        message = await communicator.receive_json_from()
        assert message == str(task.uuid)
        await delete_model_instance(task)
        message = await communicator.receive_json_from()
        assert message == str(task.uuid)
        await communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_label_added_or_removed(self):
        """Test adding or removing a label."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        task = await create_task(workspace_board_section, workspace_user)
        label = await create_label(workspace)
        resource = f"ws/task/{task.uuid}/"
        communicator = WebsocketCommunicator(websocket_application, resource)
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await add_label(label, task)
        message = await communicator.receive_json_from()
        assert message == str(task.uuid)
        await remove_label(label, task)
        message = await communicator.receive_json_from()
        assert message == str(task.uuid)
        await communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(label)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_sub_task_saved_or_deleted(self):
        """Assert event is fired when sub task is saved or deleted."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        task = await create_task(workspace_board_section, workspace_user)
        sub_task = await create_sub_task(task)
        resource = f"ws/task/{task.uuid}/"
        communicator = WebsocketCommunicator(websocket_application, resource)
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(sub_task)
        message = await communicator.receive_json_from()
        assert message == str(task.uuid)
        await delete_model_instance(sub_task)
        message = await communicator.receive_json_from()
        assert message == str(task.uuid)
        await communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_chat_message_saved_or_deleted(self):
        """Assert event is fired when chat message is saved or deleted."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        task = await create_task(workspace_board_section, workspace_user)
        chat_message = await create_chat_message(task, user)
        resource = f"ws/task/{task.uuid}/"
        communicator = WebsocketCommunicator(websocket_application, resource)
        communicator.scope["user"] = user
        connected, subprotocol = await communicator.connect()
        assert connected
        await save_model_instance(chat_message)
        message = await communicator.receive_json_from()
        assert message == str(task.uuid)
        await delete_model_instance(chat_message)
        message = await communicator.receive_json_from()
        assert message == str(task.uuid)
        await communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)
