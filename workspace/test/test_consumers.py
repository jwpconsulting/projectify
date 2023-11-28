"""Consumer tests."""
from typing import (
    TYPE_CHECKING,
    Any,
    cast,
)

from django.db import models as django_models

import pytest
from channels.db import (
    database_sync_to_async,
)
from channels.testing import (
    WebsocketCommunicator,
)

from corporate.models import Customer
from corporate.services.customer import customer_activate_subscription
from projectify.asgi import (
    websocket_application,
)
from user.factory import (
    UserFactory,
)
from workspace.models.const import WorkspaceUserRoles
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.chat_message import chat_message_create
from workspace.services.sub_task import sub_task_create
from workspace.services.workspace import workspace_add_user

from .. import (
    factory,
    models,
)

if TYPE_CHECKING:
    from user.models import User  # noqa: F401


@database_sync_to_async
def create_user() -> "User":
    """Create a user."""
    return UserFactory.create()


@database_sync_to_async
def create_workspace() -> models.Workspace:
    """Create a paid for workspace."""
    workspace = factory.WorkspaceFactory.create()
    # XXX Ideally we would use customer_create here
    customer = Customer.objects.create(workspace=workspace)
    # XXX use same fixture as in corporate/test/conftest.py
    customer_activate_subscription(
        customer=customer, stripe_customer_id="stripe_"
    )
    return workspace


@database_sync_to_async
def create_workspace_user(
    workspace: models.Workspace, user: "User"
) -> models.WorkspaceUser:
    """Create workspace user."""
    return workspace_add_user(
        workspace=workspace,
        user=user,
        role=WorkspaceUserRoles.OWNER,
    )


@database_sync_to_async
def create_workspace_board(
    workspace: models.Workspace,
) -> models.WorkspaceBoard:
    """Create workspace board."""
    return factory.WorkspaceBoardFactory.create(workspace=workspace)


@database_sync_to_async
def create_workspace_board_section(
    workspace_board: models.WorkspaceBoard,
) -> models.WorkspaceBoardSection:
    """Create workspace board section."""
    return factory.WorkspaceBoardSectionFactory.create(
        workspace_board=workspace_board,
    )


@database_sync_to_async
def create_task(
    workspace_board_section: models.WorkspaceBoardSection,
    assignee: models.WorkspaceUser,
) -> models.Task:
    """Create task."""
    return factory.TaskFactory.create(
        workspace_board_section=workspace_board_section,
        assignee=assignee,
    )


@database_sync_to_async
def create_label(workspace: models.Workspace) -> models.Label:
    """Create a label."""
    return factory.LabelFactory.create(workspace=workspace)


@database_sync_to_async
def add_label(label: models.Label, task: models.Task) -> None:
    """Add a label to a task."""
    task.add_label(label)


@database_sync_to_async
def remove_label(label: models.Label, task: models.Task) -> None:
    """Remove a label from a task."""
    task.remove_label(label)


@database_sync_to_async
def create_sub_task(
    task: models.Task, workspace_user: WorkspaceUser
) -> models.SubTask:
    """Create sub task."""
    return sub_task_create(
        task=task, who=workspace_user.user, title="don't care", done=False
    )


@database_sync_to_async
def create_chat_message(
    task: models.Task, workspace_user: models.WorkspaceUser
) -> models.ChatMessage:
    """Create chat message."""
    return chat_message_create(
        who=workspace_user.user,
        task=task,
        text="Hello world",
    )


@database_sync_to_async
def save_model_instance(model_instance: django_models.Model) -> None:
    """Save model instance."""
    model_instance.save()


@database_sync_to_async
def delete_model_instance(model_instance: django_models.Model) -> None:
    """Delete model instance."""
    model_instance.delete()


def is_workspace_message(workspace: models.Workspace, json: object) -> bool:
    """Test if the message is correct."""
    json_cast = cast(dict[str, Any], json)
    return (
        set(json_cast.keys()) == {"uuid", "type", "data"}
        and json_cast["uuid"] == str(workspace.uuid)
        and json_cast["data"]["uuid"] == str(workspace.uuid)
    )


def is_workspace_board_message(
    workspace_board: models.WorkspaceBoard, json: object
) -> bool:
    """Test if the message is correct."""
    json_cast = cast(dict[str, Any], json)
    return (
        set(json_cast.keys()) == {"uuid", "type", "data"}
        and json_cast["uuid"] == str(workspace_board.uuid)
        and json_cast["data"]["uuid"] == str(workspace_board.uuid)
    )


def is_task_message(task: models.Task, json: object) -> bool:
    """Test if the message is correct."""
    json_cast = cast(dict[str, Any], json)
    return (
        set(json_cast.keys()) == {"uuid", "type", "data"}
        and json_cast["uuid"] == str(task.uuid)
        and json_cast["data"]["uuid"] == str(task.uuid)
    )


@pytest.mark.django_db
@pytest.mark.asyncio
class TestWorkspaceConsumer:
    """Test WorkspaceConsumer."""

    async def test_workspace_saved_or_deleted(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(workspace)
        message = await communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)
        message = await communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await communicator.disconnect()

    async def test_label_saved_or_deleted(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(label)
        message = await communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(label)
        message = await communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)
        await communicator.disconnect()

    async def test_workspace_user_saved_or_deleted(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(workspace_user)
        message = await communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(workspace_user)
        message = await communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await communicator.disconnect()
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_workspace_board_saved_or_deleted(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(workspace_board)
        message = await communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(workspace_board)
        message = await communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await communicator.disconnect()
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)


@pytest.mark.django_db
@pytest.mark.asyncio
class TestWorkspaceBoardConsumer:
    """Test WorkspaceBoardConsumer."""

    async def test_workspace_board_saved_or_deleted(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(workspace_board)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await delete_model_instance(workspace_board)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await communicator.disconnect()
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_workspace_board_section_saved_or_deleted(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(workspace_board_section)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await delete_model_instance(workspace_board_section)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await communicator.disconnect()
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_task_saved_or_deleted(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(task)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await delete_model_instance(task)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_label_added_or_removed(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await add_label(label, task)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await remove_label(label, task)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(label)
        await delete_model_instance(workspace)

    async def test_sub_task_saved_or_deleted(self) -> None:
        """Test signal firing on sub task change."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        workspace_user = await create_workspace_user(workspace, user)
        task = await create_task(workspace_board_section, workspace_user)
        sub_task = await create_sub_task(task, workspace_user)
        resource = f"ws/workspace-board/{workspace_board.uuid}/"
        communicator = WebsocketCommunicator(
            websocket_application,
            resource,
        )
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(sub_task)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await delete_model_instance(sub_task)
        message = await communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
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

    async def test_task_saved_or_deleted(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(task)
        message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await delete_model_instance(task)
        message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_label_added_or_removed(self) -> None:
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
        connected, _ = await communicator.connect()
        assert connected
        await add_label(label, task)
        message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await remove_label(label, task)
        message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(label)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_sub_task_saved_or_deleted(self) -> None:
        """Assert event is fired when sub task is saved or deleted."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        task = await create_task(workspace_board_section, workspace_user)
        sub_task = await create_sub_task(task, workspace_user)
        resource = f"ws/task/{task.uuid}/"
        communicator = WebsocketCommunicator(websocket_application, resource)
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(sub_task)
        message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await delete_model_instance(sub_task)
        message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_chat_message_saved_or_deleted(self) -> None:
        """Assert event is fired when chat message is saved or deleted."""
        user = await create_user()
        workspace = await create_workspace()
        workspace_user = await create_workspace_user(workspace, user)
        workspace_board = await create_workspace_board(workspace)
        workspace_board_section = await create_workspace_board_section(
            workspace_board,
        )
        task = await create_task(workspace_board_section, workspace_user)
        chat_message = await create_chat_message(task, workspace_user)
        resource = f"ws/task/{task.uuid}/"
        communicator = WebsocketCommunicator(websocket_application, resource)
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        assert connected
        await save_model_instance(chat_message)
        message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await delete_model_instance(chat_message)
        message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)
