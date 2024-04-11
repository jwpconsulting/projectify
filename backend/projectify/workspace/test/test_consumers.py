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
# TODO
# - replace .disconnect() calls with clean_up_communicator
# - put instance .delete() calls in each fixture
import logging
from collections.abc import AsyncIterable
from typing import (
    Any,
    Union,
    cast,
)

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
from projectify.corporate.services.stripe import (
    customer_activate_subscription,
)
from projectify.user.models import User
from projectify.user.models.user_invite import UserInvite
from projectify.user.services.internal import user_create

from .. import (
    models,
)
from ..models.const import TeamMemberRoles
from ..models.label import Label
from ..models.project import Project
from ..models.section import Section
from ..models.sub_task import SubTask
from ..models.task import Task
from ..models.team_member import TeamMember
from ..models.workspace import Workspace
from ..selectors.team_member import team_member_find_for_workspace
from ..services.chat_message import chat_message_create
from ..services.label import label_create, label_delete, label_update
from ..services.project import (
    project_archive,
    project_create,
    project_delete,
    project_update,
)
from ..services.section import (
    section_create,
    section_delete,
    section_move,
    section_update,
)
from ..services.sub_task import sub_task_create, sub_task_update_many
from ..services.task import (
    task_create,
    task_create_nested,
    task_delete,
    task_move_after,
    task_update_nested,
)
from ..services.team_member import (
    team_member_delete,
    team_member_update,
)
from ..services.team_member_invite import (
    team_member_invite_create,
    team_member_invite_delete,
)
from ..services.workspace import (
    workspace_create,
    workspace_delete,
    workspace_update,
)

logger = logging.getLogger(__name__)


@pytest.fixture
async def user() -> AsyncIterable[User]:
    """Create a user."""
    user = await database_sync_to_async(user_create)(
        email="consumer-test-1@example.com"
    )
    yield user
    # TODO use a service based user deletion here
    await database_sync_to_async(user.delete)()


@pytest.fixture
async def other_user() -> AsyncIterable[User]:
    """Create another user."""
    user = await database_sync_to_async(user_create)(
        email="consumer-test-2@example.com"
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
        customer=customer,
        stripe_customer_id="stripe_",
        seats=10,
    )
    return workspace


@pytest.fixture
async def team_member(workspace: Workspace, user: User) -> TeamMember:
    """Return team member with owner status."""
    team_member = await database_sync_to_async(team_member_find_for_workspace)(
        workspace=workspace, user=user
    )
    assert team_member
    return team_member


@pytest.fixture
async def project(workspace: Workspace, user: User) -> Project:
    """Create project."""
    return await database_sync_to_async(project_create)(
        who=user,
        title="Don't care",
        workspace=workspace,
    )


@pytest.fixture
async def section(
    project: Project,
    user: User,
) -> Section:
    """Create section."""
    return await database_sync_to_async(section_create)(
        project=project,
        who=user,
        title="I am a section",
    )


@pytest.fixture
async def task(
    user: User,
    section: Section,
    team_member: TeamMember,
) -> Task:
    """Create task."""
    return await database_sync_to_async(task_create)(
        section=section,
        who=user,
        assignee=team_member,
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


HasUuid = Union[Workspace, Project, Task]


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
    resource: Union[Workspace, Project, Task], user: User
) -> WebsocketCommunicator:
    """Create a websocket communicator for a given resource and user."""
    match resource:
        case Workspace():
            url = f"ws/workspace/{resource.uuid}/"
        case Project():
            url = f"ws/project/{resource.uuid}/"
        case Task():
            url = f"ws/task/{resource.uuid}/"
    communicator = WebsocketCommunicator(websocket_application, url)
    communicator.scope["user"] = user
    headers = communicator.scope.get("headers", [])
    communicator.scope["headers"] = [
        *headers,
        [b"origin", b"http://localhost"],
    ]
    connected, code = await communicator.connect()
    if connected is False:
        await communicator.disconnect()
        raise Exception(f"Not connected: {code}")
    return communicator


async def clean_up_communicator(communicator: WebsocketCommunicator) -> None:
    """Clean up a communicator."""
    if await communicator.receive_nothing() is False:
        logger.warning("There was at least one extra message")
    await communicator.disconnect()


@pytest.fixture
async def workspace_communicator(
    workspace: Workspace, user: User
) -> WebsocketCommunicator:
    """Return a communicator to a workspace instance."""
    return await make_communicator(workspace, user)


@pytest.fixture
async def project_communicator(
    project: Project, user: User
) -> WebsocketCommunicator:
    """Return a communicator to a project instance."""
    return await make_communicator(project, user)


@pytest.fixture
async def task_communicator(task: Task, user: User) -> WebsocketCommunicator:
    """Return a communicator to a task instance."""
    return await make_communicator(task, user)


class TestWorkspace:
    """Test consumer behavior for Workspace changes."""

    async def test_not_found(self, user: User, other_user: User) -> None:
        """Test we can't connect to an unrelated workspace's consumer."""
        workspace = await database_sync_to_async(workspace_create)(
            owner=user, title="A workspace"
        )
        with pytest.raises(Exception) as e:
            await make_communicator(workspace, other_user)
        assert e.match("Not connected: 404")
        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )

    async def test_workspace_life_cycle(
        self,
        user: User,
    ) -> None:
        """Test signal firing on workspace change."""
        workspace = await database_sync_to_async(workspace_create)(
            owner=user,
            title="A workspace",
        )

        workspace_communicator = await make_communicator(workspace, user)

        await database_sync_to_async(workspace_update)(
            workspace=workspace,
            who=user,
            title="A new hope",
        )
        assert await expect_message(workspace_communicator, workspace)

        await database_sync_to_async(workspace_delete)(
            who=user,
            workspace=workspace,
        )
        await clean_up_communicator(workspace_communicator)


class TestTeamMember:
    """Test consumer behavior for TeamMember changes."""

    async def test_team_member_life_cycle(
        self,
        user: User,
        workspace: Workspace,
        team_member: TeamMember,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test signal firing on team member save or delete."""
        other_user = await database_sync_to_async(user_create)(
            email="hello-world@example.com"
        )
        # New team member
        other_team_member = await database_sync_to_async(
            team_member_invite_create
        )(
            workspace=workspace,
            email_or_user=other_user,
            who=user,
        )
        assert isinstance(other_team_member, TeamMember)
        await expect_message(workspace_communicator, workspace)
        # Team member updated
        await database_sync_to_async(team_member_update)(
            team_member=other_team_member,
            who=user,
            role=TeamMemberRoles.OBSERVER,
        )
        await expect_message(workspace_communicator, workspace)

        # TODO user updated (picture/name)

        # Team member deleted (delete initial ws user as well)
        await database_sync_to_async(team_member_delete)(
            team_member=other_team_member,
            who=user,
        )
        await expect_message(workspace_communicator, workspace)

        # Now we invite someone without an account:
        await database_sync_to_async(team_member_invite_create)(
            workspace=workspace,
            email_or_user="doesnotexist@example.com",
            who=user,
        )
        await expect_message(workspace_communicator, workspace)

        # And we remove their invitation
        await database_sync_to_async(team_member_invite_delete)(
            workspace=workspace,
            email="doesnotexist@example.com",
            who=user,
        )
        await expect_message(workspace_communicator, workspace)

        # With only one remaining user, we call workspace_delete instead
        await database_sync_to_async(workspace_delete)(
            workspace=workspace,
            who=user,
        )
        # Before we would expect a message here, but now we disconnect when a
        # workspace is deleted
        await clean_up_communicator(workspace_communicator)

        # Clean up user invite
        await UserInvite.objects.all().adelete()


class TestProject:
    """Test consumer behavior for Project changes."""

    async def test_not_found(
        self,
        workspace: Workspace,
        user: User,
        other_user: User,
        team_member: TeamMember,
    ) -> None:
        """Test we can't connect to an unrelated project's consumer."""
        project = await database_sync_to_async(project_create)(
            who=user, workspace=workspace, title=""
        )
        with pytest.raises(Exception) as e:
            await make_communicator(project, other_user)
        assert e.match("Not connected: 404")

        await database_sync_to_async(project_delete)(who=user, project=project)
        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )

    async def test_project_life_cycle(
        self,
        user: User,
        workspace: Workspace,
        team_member: TeamMember,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test workspace / board consumer behavior for board changes."""
        # Create
        project = await database_sync_to_async(project_create)(
            who=user,
            workspace=workspace,
            title="It's time to chew bubble gum and write Django",
            description="And I'm all out of Django",
        )
        assert await expect_message(workspace_communicator, workspace)

        project_communicator = await make_communicator(project, user)

        # Update
        await database_sync_to_async(project_update)(
            who=user,
            project=project,
            title="don't care",
        )
        assert await expect_message(project_communicator, project)
        assert await expect_message(workspace_communicator, workspace)

        # Archive
        await database_sync_to_async(project_archive)(
            who=user,
            project=project,
            archived=True,
        )
        assert await expect_message(workspace_communicator, workspace)

        # Delete
        await database_sync_to_async(project_delete)(
            who=user,
            project=project,
        )
        assert await expect_message(workspace_communicator, workspace)

        await clean_up_communicator(workspace_communicator)
        await clean_up_communicator(project_communicator)

        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )


class TestSection:
    """Test section behavior."""

    async def test_section_life_cycle(
        self,
        user: User,
        workspace: Workspace,
        team_member: TeamMember,
        project: Project,
        project_communicator: WebsocketCommunicator,
    ) -> None:
        """Test project consumer behavior for section changes."""
        # Create it
        section = await database_sync_to_async(section_create)(
            who=user,
            title="A section",
            project=project,
        )
        assert await expect_message(project_communicator, project)

        # Update it
        await database_sync_to_async(section_update)(
            who=user,
            section=section,
            title="Title has changed",
        )
        assert await expect_message(project_communicator, project)

        # Move it
        await database_sync_to_async(section_move)(
            who=user,
            section=section,
            order=0,
        )
        assert await expect_message(project_communicator, project)

        # Delete it
        await database_sync_to_async(section_delete)(
            who=user,
            section=section,
        )
        assert await expect_message(project_communicator, project)

        # XXX Might be able to disconnect after project_delete as well
        await project_communicator.disconnect()
        await database_sync_to_async(project_delete)(who=user, project=project)
        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )


class TestLabel:
    """Test consumer behavior for label changes."""

    async def test_label_life_cycle(
        self,
        workspace: Workspace,
        team_member: TeamMember,
        user: User,
        workspace_communicator: WebsocketCommunicator,
    ) -> None:
        """Test that workspace consumer fires on label changes."""
        # Create
        label = await database_sync_to_async(label_create)(
            who=user,
            workspace=workspace,
            color=0,
            name="hello",
        )
        assert await expect_message(workspace_communicator, workspace)
        # Update
        await database_sync_to_async(label_update)(
            who=user,
            label=label,
            color=1,
            name="updated",
        )
        assert await expect_message(workspace_communicator, workspace)

        # Delete
        await database_sync_to_async(label_delete)(
            who=user,
            label=label,
        )
        assert await expect_message(workspace_communicator, workspace)

        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )
        await workspace_communicator.disconnect()


class TestTask:
    """Test consumer behavior for tasks."""

    async def test_not_found(
        self,
        user: User,
        other_user: User,
        section: Section,
        project: Project,
        team_member: TeamMember,
        workspace: Workspace,
    ) -> None:
        """Test we can't connect to an unrelated task's consumer."""
        del team_member
        task = await database_sync_to_async(task_create_nested)(
            who=user,
            section=section,
            title="A task",
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
            labels=[],
        )
        with pytest.raises(Exception) as e:
            await make_communicator(task, other_user)
        assert e.match("Not connected: 404")
        await database_sync_to_async(task_delete)(who=user, task=task)
        await database_sync_to_async(section_delete)(who=user, section=section)
        await database_sync_to_async(project_delete)(who=user, project=project)
        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )

    async def test_task_life_cycle(
        self,
        user: User,
        workspace: Workspace,
        team_member: TeamMember,
        project: Project,
        section: Section,
        project_communicator: WebsocketCommunicator,
    ) -> None:
        """Test that board and task consumer fire."""
        # Create
        task = await database_sync_to_async(task_create_nested)(
            who=user,
            section=section,
            title="A task",
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
            labels=[],
        )
        assert await expect_message(project_communicator, project)

        task_communicator = await make_communicator(task, user)

        # Update
        await database_sync_to_async(task_update_nested)(
            who=user,
            task=task,
            title="A task",
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
            labels=[],
        )
        assert await expect_message(project_communicator, project)
        assert await expect_message(task_communicator, task)

        # Move
        await database_sync_to_async(task_move_after)(
            who=user,
            task=task,
            after=section,
        )
        assert await expect_message(project_communicator, project)
        assert await expect_message(task_communicator, task)

        # Delete
        await database_sync_to_async(task_delete)(
            who=user,
            task=task,
        )
        assert await expect_message(project_communicator, project)

        await clean_up_communicator(project_communicator)
        # Ideally, a task consumer will disconnect when a task is deleted
        await clean_up_communicator(task_communicator)

        await database_sync_to_async(section_delete)(who=user, section=section)
        await database_sync_to_async(project_delete)(who=user, project=project)
        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )


class TestTaskLabel:
    """Test consumer behavior for task labels."""

    async def test_label_added_or_removed(
        self,
        user: User,
        workspace: Workspace,
        team_member: TeamMember,
        label: Label,
        project: Project,
        section: Section,
        task: Task,
        project_communicator: WebsocketCommunicator,
        task_communicator: WebsocketCommunicator,
    ) -> None:
        """Test that project and task consumer fire."""
        # Add label
        await database_sync_to_async(task_update_nested)(
            who=user,
            task=task,
            title=task.title,
            labels=[label],
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
        )
        assert await expect_message(project_communicator, project)
        assert await expect_message(task_communicator, task)

        # Remove label
        await database_sync_to_async(task_update_nested)(
            who=user,
            task=task,
            title=task.title,
            labels=[],
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
        )
        assert await expect_message(project_communicator, project)
        assert await expect_message(task_communicator, task)

        await project_communicator.disconnect()
        await task_communicator.disconnect()

        await database_sync_to_async(section_delete)(who=user, section=section)
        await database_sync_to_async(project_delete)(who=user, project=project)
        await database_sync_to_async(label_delete)(who=user, label=label)
        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )


class TestSubTask:
    """Test consumer behavior for sub tasks."""

    async def test_sub_task_saved_or_deleted_project(
        self,
        user: User,
        workspace: Workspace,
        team_member: TeamMember,
        project: Project,
        section: Section,
        task: Task,
        sub_task: SubTask,
        project_communicator: WebsocketCommunicator,
        task_communicator: WebsocketCommunicator,
    ) -> None:
        """Test that project and task consumer fire."""
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
        assert await expect_message(project_communicator, project)
        assert await expect_message(task_communicator, task)

        # Simulate removing a task
        await database_sync_to_async(sub_task_update_many)(
            who=user,
            task=task,
            sub_tasks=[sub_task],
            create_sub_tasks=[],
            update_sub_tasks=[],
        )
        assert await expect_message(project_communicator, project)
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
        assert await expect_message(project_communicator, project)
        assert await expect_message(task_communicator, task)

        await project_communicator.disconnect()
        await task_communicator.disconnect()

        await database_sync_to_async(task_delete)(who=user, task=task)
        await database_sync_to_async(section_delete)(who=user, section=section)
        await database_sync_to_async(project_delete)(who=user, project=project)
        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )


class TestChatMessage:
    """Test consumer behavior for chat messages."""

    async def test_chat_message_saved_or_deleted(
        self,
        user: User,
        workspace: Workspace,
        team_member: TeamMember,
        project: Project,
        section: Section,
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
        # so no chat_message_delete service exists, and we don't have to delete
        # it either
        await task_communicator.disconnect()
        await database_sync_to_async(task_delete)(who=user, task=task)
        await database_sync_to_async(section_delete)(who=user, section=section)
        await database_sync_to_async(project_delete)(who=user, project=project)
        await database_sync_to_async(workspace_delete)(
            who=user, workspace=workspace
        )
