# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022-2024 JWP Consulting GK
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
"""Consumer tests."""
from typing import (
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

from corporate.services.customer import customer_activate_subscription
from projectify.asgi import (
    websocket_application,
)
from user.models import User
from user.services.user import user_create
from workspace.models.label import Label
from workspace.models.sub_task import SubTask
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser
from workspace.selectors.workspace_user import (
    workspace_user_find_for_workspace,
)
from workspace.services.chat_message import chat_message_create
from workspace.services.label import label_create
from workspace.services.sub_task import sub_task_create
from workspace.services.task import task_create
from workspace.services.workspace import workspace_create
from workspace.services.workspace_board import workspace_board_create
from workspace.services.workspace_board_section import (
    workspace_board_section_create,
)

from .. import (
    models,
)


@pytest.fixture
async def user() -> User:
    """Create a user."""
    return await database_sync_to_async(user_create)(
        email="consumer-test@example.com"
    )


@pytest.fixture
async def workspace(user: User) -> models.Workspace:
    """Create a paid for workspace."""
    workspace = await database_sync_to_async(workspace_create)(
        title="Workspace title",
        owner=user,
    )
    customer = workspace.customer
    # XXX use same fixture as in corporate/test/conftest.py
    await database_sync_to_async(customer_activate_subscription)(
        customer=customer, stripe_customer_id="stripe_"
    )
    return workspace


@pytest.fixture
async def workspace_user(workspace: Workspace, user: User) -> WorkspaceUser:
    """Return workspace user with owner status."""
    workspace_user = await database_sync_to_async(
        workspace_user_find_for_workspace
    )(workspace=workspace, user=user)
    assert workspace_user
    return workspace_user


@pytest.fixture
async def workspace_board(workspace: Workspace, user: User) -> WorkspaceBoard:
    """Create workspace board."""
    return await database_sync_to_async(workspace_board_create)(
        who=user,
        title="Don't care",
        workspace=workspace,
    )


@pytest.fixture
async def workspace_board_section(
    workspace_board: WorkspaceBoard,
    user: User,
) -> WorkspaceBoardSection:
    """Create workspace board section."""
    return await database_sync_to_async(workspace_board_section_create)(
        workspace_board=workspace_board,
        who=user,
        title="I am a workspace board section",
    )


@pytest.fixture
async def task(
    user: User,
    workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
) -> Task:
    """Create task."""
    return await database_sync_to_async(task_create)(
        workspace_board_section=workspace_board_section,
        who=user,
        assignee=workspace_user,
        title="I am a task",
    )


@pytest.fixture
async def label(workspace: Workspace, user: User) -> Label:
    """Create a label."""
    return await database_sync_to_async(label_create)(
        workspace=workspace,
        who=user,
        color=0,
        name="don't care",
    )


@database_sync_to_async
def add_label(label: models.Label, task: models.Task) -> None:
    """Add a label to a task."""
    task.add_label(label)


@database_sync_to_async
def remove_label(label: models.Label, task: models.Task) -> None:
    """Remove a label from a task."""
    task.remove_label(label)


@pytest.fixture
async def sub_task(task: Task, user: User) -> SubTask:
    """Create sub task."""
    return await database_sync_to_async(sub_task_create)(
        task=task, who=user, title="don't care", done=False
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
    return set(json_cast.keys()) == {"uuid", "type", "data"} and json_cast[
        "uuid"
    ] == str(workspace.uuid)


def is_workspace_board_message(
    workspace_board: models.WorkspaceBoard, json: object
) -> bool:
    """Test if the message is correct."""
    json_cast = cast(dict[str, Any], json)
    return set(json_cast.keys()) == {"uuid", "type", "data"} and json_cast[
        "uuid"
    ] == str(workspace_board.uuid)


def is_task_message(task: models.Task, json: object) -> bool:
    """Test if the message is correct."""
    json_cast = cast(dict[str, Any], json)
    return set(json_cast.keys()) == {"uuid", "type", "data"} and json_cast[
        "uuid"
    ] == str(task.uuid)


pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


async def make_communicator(
    resource: str, user: User
) -> WebsocketCommunicator:
    """Create a websocket communicator for a given resource and user."""
    communicator = WebsocketCommunicator(websocket_application, resource)
    communicator.scope["user"] = user
    connected, _maybe_code = await communicator.connect()
    assert connected, _maybe_code
    return communicator


@pytest.fixture
async def workspace_communicator(
    workspace: Workspace, user: User
) -> WebsocketCommunicator:
    """Return a communicator to a workspace instance."""
    return await make_communicator(f"ws/workspace/{workspace.uuid}/", user)


@pytest.fixture
async def workspace_board_communicator(
    workspace_board: WorkspaceBoard, user: User
) -> WebsocketCommunicator:
    """Return a communicator to a workspace board instance."""
    return await make_communicator(
        f"ws/workspace-board/{workspace_board.uuid}/", user
    )


@pytest.fixture
async def task_communicator(task: Task, user: User) -> WebsocketCommunicator:
    """Return a communicator to a task instance."""
    return await make_communicator(f"ws/task/{task.uuid}/", user)


class TestWorkspaceConsumer:
    """Test WorkspaceConsumer."""

    async def test_workspace_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on workspace change."""
        await save_model_instance(workspace)
        message = await workspace_communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)
        message = await workspace_communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await workspace_communicator.disconnect()
        # If we delete the user before disconnecting, we're in trouble
        await delete_model_instance(user)

    async def test_label_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        label: Label,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on workspace change."""
        await save_model_instance(label)
        message = await workspace_communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(label)
        message = await workspace_communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)
        await workspace_communicator.disconnect()
        await delete_model_instance(user)

    async def test_workspace_user_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on workspace user save or delete."""
        await save_model_instance(workspace_user)
        message = await workspace_communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(workspace_user)
        message = await workspace_communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await workspace_communicator.disconnect()
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_workspace_board_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on workspace board change."""
        await save_model_instance(workspace_board)
        message = await workspace_communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await delete_model_instance(workspace_board)
        message = await workspace_communicator.receive_json_from()
        assert is_workspace_message(workspace, message)
        await workspace_communicator.disconnect()
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)


class TestWorkspaceBoardConsumer:
    """Test WorkspaceBoardConsumer."""

    async def test_workspace_board_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on workspace board change."""
        await save_model_instance(workspace_board)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await delete_model_instance(workspace_board)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await workspace_board_communicator.disconnect()
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_workspace_board_section_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        workspace_board_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on workspace board section change."""
        await save_model_instance(workspace_board_section)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await delete_model_instance(workspace_board_section)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await workspace_board_communicator.disconnect()
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_task_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        task: Task,
        workspace_board_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on task change."""
        await save_model_instance(task)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await delete_model_instance(task)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await workspace_board_communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_label_added_or_removed(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        label: Label,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        task: Task,
        workspace_board_communicator: WebsocketCommunicator,
    ) -> None:
        """Test workspace board update on task label add or remove."""
        await add_label(label, task)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await remove_label(label, task)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await workspace_board_communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(label)
        await delete_model_instance(workspace)

    async def test_sub_task_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        task: Task,
        sub_task: SubTask,
        workspace_board_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on sub task change."""
        await save_model_instance(sub_task)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await delete_model_instance(sub_task)
        message = await workspace_board_communicator.receive_json_from()
        assert is_workspace_board_message(workspace_board, message)
        await workspace_board_communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)


class TestTaskConsumer:
    """Test TaskConsumer."""

    async def test_task_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        task: Task,
        task_communicator: WebsocketCommunicator,
    ) -> None:
        """Assert event is fired when task is saved or deleted."""
        await delete_model_instance(task)
        message = await task_communicator.receive_json_from()
        assert is_task_message(task, message)
        await task_communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_label_added_or_removed(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        label: Label,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        task: Task,
        task_communicator: WebsocketCommunicator,
    ) -> None:
        """Test adding or removing a label."""
        await remove_label(label, task)
        message = await task_communicator.receive_json_from()
        assert is_task_message(task, message)
        await task_communicator.disconnect()
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(label)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_sub_task_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        task: Task,
        sub_task: SubTask,
        task_communicator: WebsocketCommunicator,
    ) -> None:
        """Assert event is fired when sub task is saved or deleted."""
        await delete_model_instance(sub_task)
        message = await task_communicator.receive_json_from()
        assert is_task_message(task, message)
        await task_communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)

    async def test_chat_message_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        task: Task,
        task_communicator: WebsocketCommunicator,
    ) -> None:
        """Assert event is fired when chat message is saved or deleted."""
        await database_sync_to_async(chat_message_create)(
            who=user,
            task=task,
            text="Hello world",
        )
        message = await task_communicator.receive_json_from()
        assert is_task_message(task, message)
        # TODO chat messages are not supported right now,
        # so no chat_message_delete service exists.
        # await delete_model_instance(chat_message)
        # message = await communicator.receive_json_from()
        assert is_task_message(task, message)
        await task_communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(user)
        await delete_model_instance(workspace)
