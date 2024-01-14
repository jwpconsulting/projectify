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
import logging
from collections.abc import AsyncIterable
from typing import (
    Any,
    Union,
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
from workspace.services.sub_task import sub_task_create, sub_task_update_many
from workspace.services.task import (
    task_create,
    task_create_nested,
    task_delete,
    task_move_after,
    task_update_nested,
)
from workspace.services.workspace import workspace_create
from workspace.services.workspace_board import workspace_board_create
from workspace.services.workspace_board_section import (
    workspace_board_section_create,
    workspace_board_section_delete,
    workspace_board_section_move,
    workspace_board_section_update,
)

from .. import (
    models,
)

logger = logging.getLogger(__name__)


@pytest.fixture
async def user() -> AsyncIterable[User]:
    """Create a user."""
    user = await database_sync_to_async(user_create)(
        email="consumer-test@example.com"
    )
    yield user
    # TODO use a service based user deletion here
    await database_sync_to_async(user.delete)()


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


HasUuid = Union[Workspace, WorkspaceBoard, Task]


async def expect_message(
    communicator: WebsocketCommunicator, has_uuid: HasUuid
) -> bool:
    """Test if the message is correct."""
    json = await communicator.receive_json_from()
    json_cast = cast(dict[str, Any], json)
    logger.info("Received message %s for %s", json_cast["type"], has_uuid)
    return set(json_cast.keys()) == {"uuid", "type", "data"} and json_cast[
        "uuid"
    ] == str(has_uuid.uuid)


pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


async def make_communicator(
    resource: Union[Workspace, WorkspaceBoard, Task], user: User
) -> WebsocketCommunicator:
    """Create a websocket communicator for a given resource and user."""
    match resource:
        case Workspace():
            url = f"ws/workspace/{resource.uuid}/"
        case WorkspaceBoard():
            url = f"ws/workspace-board/{resource.uuid}/"
        case Task():
            url = f"ws/task/{resource.uuid}/"
    communicator = WebsocketCommunicator(websocket_application, url)
    communicator.scope["user"] = user
    connected, _maybe_code = await communicator.connect()
    assert connected, _maybe_code
    return communicator


async def clean_up_communicator(communicator: WebsocketCommunicator) -> None:
    """Clean up a communicator."""
    if await communicator.receive_nothing() is True:
        logger.warn("There was at least one extra message")
    await communicator.disconnect()


@pytest.fixture
async def workspace_communicator(
    workspace: Workspace, user: User
) -> WebsocketCommunicator:
    """Return a communicator to a workspace instance."""
    return await make_communicator(workspace, user)


@pytest.fixture
async def workspace_board_communicator(
    workspace_board: WorkspaceBoard, user: User
) -> WebsocketCommunicator:
    """Return a communicator to a workspace board instance."""
    return await make_communicator(workspace_board, user)


@pytest.fixture
async def task_communicator(task: Task, user: User) -> WebsocketCommunicator:
    """Return a communicator to a task instance."""
    return await make_communicator(task, user)


class TestWorkspace:
    """Test consumer behavior for Workspace changes."""

    async def test_workspace_saved_or_deleted(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on workspace change."""
        await save_model_instance(workspace)
        assert await expect_message(workspace_communicator, workspace)
        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)
        assert await expect_message(workspace_communicator, workspace)
        await workspace_communicator.disconnect()


class TestWorkspaceUser:
    """Test consumer behavior for WorkspaceUser changes."""

    async def test_workspace_user_saved_or_deleted(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on workspace user save or delete."""
        await save_model_instance(workspace_user)
        assert await expect_message(workspace_communicator, workspace)

        await delete_model_instance(workspace_user)
        assert await expect_message(workspace_communicator, workspace)

        await workspace_communicator.disconnect()
        await delete_model_instance(workspace)


class TestWorkspaceBoard:
    """Test consumer behavior for WorkspaceBoard changes."""

    async def test_workspace_board_saved_or_deleted(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_communicator: WebsocketCommunicator,
        workspace_board_communicator: WebsocketCommunicator,
    ) -> None:
        """Test workspace / board consumer behavior for board changes."""
        await save_model_instance(workspace_board)
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(workspace_communicator, workspace)

        await delete_model_instance(workspace_board)
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(workspace_communicator, workspace)

        await workspace_communicator.disconnect()
        await workspace_board_communicator.disconnect()
        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)


class TestWorkspaceBoardSection:
    """Test workspace board section behavior."""

    async def test_workspace_board_section_life_cycle(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_communicator: WebsocketCommunicator,
    ) -> None:
        """Test workspace board consumer behavior for section changes."""
        # Create it
        workspace_board_section = await database_sync_to_async(
            workspace_board_section_create
        )(
            who=user,
            title="A workspace board section",
            workspace_board=workspace_board,
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )

        # Update it
        await database_sync_to_async(workspace_board_section_update)(
            who=user,
            workspace_board_section=workspace_board_section,
            title="Title has changed",
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )

        # Move it
        await database_sync_to_async(workspace_board_section_move)(
            who=user,
            workspace_board_section=workspace_board_section,
            order=0,
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )

        # Delete it
        await database_sync_to_async(workspace_board_section_delete)(
            who=user,
            workspace_board_section=workspace_board_section,
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )

        await workspace_board_communicator.disconnect()
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)


class TestLabel:
    """Test consumer behavior for label changes."""

    async def test_label_saved_or_deleted(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        label: Label,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test that workspace consumer fires on label changes."""
        await save_model_instance(label)
        assert await expect_message(workspace_communicator, workspace)

        await delete_model_instance(label)
        assert await expect_message(workspace_communicator, workspace)

        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)
        await workspace_communicator.disconnect()


class TestTaskConsumer:
    """Test consumer behavior for tasks."""

    async def test_task_life_cycle(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        workspace_board_communicator: WebsocketCommunicator,
    ) -> None:
        """Test that board and task consumer fire."""
        # Create
        task = await database_sync_to_async(task_create_nested)(
            who=user,
            workspace_board_section=workspace_board_section,
            title="A task",
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
            labels=[],
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )

        task_communicator = await make_communicator(task, user)

        # Update
        await database_sync_to_async(task_update_nested)(
            who=user,
            task=task,
            title="A task",
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
            labels=[],
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(task_communicator, task)

        # Move
        await database_sync_to_async(task_move_after)(
            who=user,
            task=task,
            after=workspace_board_section,
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(task_communicator, task)

        # Delete
        await database_sync_to_async(task_delete)(
            who=user,
            task=task,
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(task_communicator, task)

        await clean_up_communicator(workspace_board_communicator)
        # Ideally, a task consumer will disconnect when a task is deleted
        await clean_up_communicator(task_communicator)

        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)


class TestTaskLabel:
    """Test consumer behavior for task labels."""

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
        task_communicator: WebsocketCommunicator,
    ) -> None:
        """Test that workspace board and task consumer fire."""
        # Add label
        await database_sync_to_async(task_update_nested)(
            who=user,
            task=task,
            title=task.title,
            labels=[label],
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(task_communicator, task)

        # Remove label
        await database_sync_to_async(task_update_nested)(
            who=user,
            task=task,
            title=task.title,
            labels=[],
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(task_communicator, task)

        await workspace_board_communicator.disconnect()
        await task_communicator.disconnect()

        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(label)
        await delete_model_instance(workspace)


class TestSubTask:
    """Test consumer behavior for sub tasks."""

    async def test_sub_task_saved_or_deleted_workspace_board(
        self,
        user: User,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace_board_section: WorkspaceBoardSection,
        task: Task,
        sub_task: SubTask,
        workspace_board_communicator: WebsocketCommunicator,
        task_communicator: WebsocketCommunicator,
    ) -> None:
        """Test that workspace board and task consumer fire."""
        # Simulate editing a task
        await database_sync_to_async(sub_task_update_many)(
            who=user,
            task=task,
            sub_tasks=[sub_task],
            create_sub_tasks=[],
            update_sub_tasks=[
                {
                    "uuid": sub_task.uuid,
                    "title": sub_task.title,
                    "done": False,
                    "_order": 0,
                }
            ],
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(task_communicator, task)

        # Simulate removing a task
        await database_sync_to_async(sub_task_update_many)(
            who=user,
            task=task,
            sub_tasks=[sub_task],
            create_sub_tasks=[],
            update_sub_tasks=[],
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(task_communicator, task)

        # Simulate adding a task
        await database_sync_to_async(sub_task_update_many)(
            who=user,
            task=task,
            sub_tasks=[],
            create_sub_tasks=[
                {"title": "to do", "done": False, "_order": 0},
            ],
            update_sub_tasks=[],
        )
        assert await expect_message(
            workspace_board_communicator, workspace_board
        )
        assert await expect_message(task_communicator, task)

        await workspace_board_communicator.disconnect()
        await task_communicator.disconnect()

        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)


class TestChatMessage:
    """Test consumer behavior for chat messages."""

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
        assert await expect_message(task_communicator, task)
        # TODO chat messages are not supported right now,
        # so no chat_message_delete service exists.
        # await delete_model_instance(chat_message)
        # message = await communicator.receive_json_from()
        await task_communicator.disconnect()
        await delete_model_instance(task)
        await delete_model_instance(workspace_board_section)
        await delete_model_instance(workspace_board)
        await delete_model_instance(workspace_user)
        await delete_model_instance(workspace)
