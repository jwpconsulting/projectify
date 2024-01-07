# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
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
Workspace test fixtures.

Fixture name convention

- the_thing: Fixture for a model instance
- other_the_thing: Fixture for a model instance belonging to the same workspace
- other_other_the_thing: Fixture for yet another model instance belonging to
  the same workspace
- unrelated_the_thing: Fixture for a model instance belonging to another
  workspace

Anything that is unrelated can be used to test if users see only objects that
they are allowed to see.
"""
from datetime import (
    datetime,
)
from datetime import (
    timezone as dt_timezone,
)

from django.utils import (
    timezone,
)

import pytest
from faker import Faker

from corporate.services.customer import customer_activate_subscription
from user.models import User, UserInvite
from workspace.models.label import Label
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser
from workspace.models.workspace_user_invite import (
    WorkspaceUserInvite,
)
from workspace.selectors.workspace_user import (
    workspace_user_find_for_workspace,
)
from workspace.services.chat_message import chat_message_create
from workspace.services.label import label_create
from workspace.services.sub_task import sub_task_create
from workspace.services.task import task_create
from workspace.services.workspace import workspace_add_user, workspace_create
from workspace.services.workspace_board import (
    workspace_board_archive,
    workspace_board_create,
)
from workspace.services.workspace_board_section import (
    workspace_board_section_create,
)
from workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
)

from .. import (
    models,
)


@pytest.fixture
def now() -> datetime:
    """Return now."""
    return timezone.now()


@pytest.fixture
def workspace(faker: Faker, user: User) -> models.Workspace:
    """Return workspace."""
    workspace = workspace_create(
        title=faker.company(),
        description=faker.paragraph(),
        owner=user,
    )
    customer = workspace.customer
    # XXX use same fixture as in corporate/test/conftest.py
    customer_activate_subscription(
        customer=customer, stripe_customer_id="stripe_"
    )
    # TODO right now our tests depend on the workspace being paid for
    # We should also be able to test most actions here for a workspace that
    # isn't paid.
    return workspace


@pytest.fixture
def unrelated_workspace(
    faker: Faker, unrelated_user: User
) -> models.Workspace:
    """Return workspace."""
    workspace = workspace_create(
        title=faker.company(),
        description=faker.paragraph(),
        owner=unrelated_user,
    )
    customer = workspace.customer
    # XXX use same fixture as in corporate/test/conftest.py
    customer_activate_subscription(
        customer=customer, stripe_customer_id="stripe_"
    )
    # TODO right now our tests depend on the workspace being paid for
    # We should also be able to test most actions here for a workspace that
    # isn't paid.
    return workspace


@pytest.fixture
def workspace_user_invite(
    workspace: models.Workspace,
    workspace_user: WorkspaceUser,
    # TODO user_invite needed to redeem invite, right? verify.
    user_invite: UserInvite,
    faker: Faker,
) -> models.WorkspaceUserInvite:
    """Return workspace user invite."""
    email: str = faker.email()
    invite = add_or_invite_workspace_user(
        who=workspace_user.user, workspace=workspace, email_or_user=email
    )
    assert isinstance(invite, WorkspaceUserInvite)
    return invite


@pytest.fixture
def workspace_user(
    workspace: models.Workspace, user: User
) -> models.WorkspaceUser:
    """Return workspace user with owner status."""
    workspace_user = workspace_user_find_for_workspace(
        workspace=workspace, user=user
    )
    assert workspace_user
    return workspace_user


@pytest.fixture
def other_workspace_user(
    workspace: models.Workspace, other_user: User
) -> models.WorkspaceUser:
    """Return workspace user for other_user."""
    workspace_user = workspace_add_user(
        workspace=workspace,
        user=other_user,
        role=models.WorkspaceUserRoles.OWNER,
    )
    assert workspace_user
    return workspace_user


@pytest.fixture
def unrelated_workspace_user(
    unrelated_workspace: models.Workspace, unrelated_user: User
) -> models.WorkspaceUser:
    """Return workspace user for other_user."""
    workspace_user = workspace_user_find_for_workspace(
        workspace=unrelated_workspace, user=unrelated_user
    )
    assert workspace_user
    return workspace_user


@pytest.fixture
def workspace_board(
    other_workspace_user: WorkspaceUser,
    faker: Faker,
    workspace: models.Workspace,
) -> models.WorkspaceBoard:
    """Return workspace board."""
    return workspace_board_create(
        who=other_workspace_user.user,
        title=faker.text(),
        description=faker.paragraph(),
        workspace=workspace,
        deadline=faker.date_time(tzinfo=dt_timezone.utc)
        if faker.pybool()
        else None,
    )


@pytest.fixture
def unrelated_workspace_board(
    unrelated_workspace_user: WorkspaceUser,
    faker: Faker,
    unrelated_workspace: models.Workspace,
) -> models.WorkspaceBoard:
    """Return an unrelated workspace board."""
    return workspace_board_create(
        who=unrelated_workspace_user.user,
        title=faker.text(),
        description=faker.paragraph(),
        workspace=unrelated_workspace,
        # XXX another victim to non-determinism
        deadline=faker.date_time(tzinfo=dt_timezone.utc),
    )


@pytest.fixture
def archived_workspace_board(
    workspace: models.Workspace,
    now: datetime,
    other_workspace_user: WorkspaceUser,
    faker: Faker,
) -> models.WorkspaceBoard:
    """Return archived workspace board."""
    workspace_board = workspace_board_create(
        who=other_workspace_user.user,
        title=faker.text(),
        description=faker.paragraph(),
        workspace=workspace,
    )
    workspace_board_archive(
        who=other_workspace_user.user,
        workspace_board=workspace_board,
        archived=True,
    )
    return workspace_board


@pytest.fixture
def workspace_board_section(
    workspace_board: models.WorkspaceBoard,
    # Another workspace user creates it, so that we can correctly assess
    # permissions and not implicitly associate the main user with this
    # workspace
    other_workspace_user: WorkspaceUser,
    faker: Faker,
) -> models.WorkspaceBoardSection:
    """Return workspace board section."""
    return workspace_board_section_create(
        who=other_workspace_user.user,
        workspace_board=workspace_board,
        title=faker.sentence(),
    )


@pytest.fixture
def other_workspace_board_section(
    workspace_board: models.WorkspaceBoard,
    workspace_user: WorkspaceUser,
    faker: Faker,
) -> models.WorkspaceBoardSection:
    """Create another workspace board section."""
    return workspace_board_section_create(
        who=workspace_user.user,
        workspace_board=workspace_board,
        title=faker.sentence(),
    )


@pytest.fixture
def other_other_workspace_board_section(
    workspace_board: models.WorkspaceBoard,
    workspace_user: WorkspaceUser,
    faker: Faker,
) -> models.WorkspaceBoardSection:
    """Create yet another workspace board section."""
    return workspace_board_section_create(
        who=workspace_user.user,
        workspace_board=workspace_board,
        title=faker.sentence(),
    )


@pytest.fixture
def unrelated_workspace_board_section(
    unrelated_workspace_board: models.WorkspaceBoard,
    unrelated_workspace_user: WorkspaceUser,
    faker: Faker,
) -> models.WorkspaceBoardSection:
    """Return unrelated workspace board section."""
    return workspace_board_section_create(
        who=unrelated_workspace_user.user,
        workspace_board=unrelated_workspace_board,
        title=faker.sentence(),
    )


@pytest.fixture
def task(
    workspace_board_section: models.WorkspaceBoardSection,
    workspace_user: models.WorkspaceUser,
    faker: Faker,
) -> models.Task:
    """Return task."""
    return task_create(
        who=workspace_user.user,
        workspace_board_section=workspace_board_section,
        title=faker.sentence(),
        description=faker.paragraph(),
        assignee=workspace_user if faker.pybool() else None,
        deadline=faker.date_time(tzinfo=dt_timezone.utc),
    )


@pytest.fixture
def other_task(
    workspace_board_section: models.WorkspaceBoardSection,
    workspace_user: models.WorkspaceUser,
) -> models.Task:
    """Return another task belonging to the same workspace board section."""
    return task_create(
        who=workspace_user.user,
        workspace_board_section=workspace_board_section,
        title="I am the other task",
    )


@pytest.fixture
def unrelated_task(
    unrelated_workspace_board_section: models.WorkspaceBoardSection,
    unrelated_workspace_user: models.WorkspaceUser,
) -> models.Task:
    """Return another task belonging to the same workspace board section."""
    return task_create(
        who=unrelated_workspace_user.user,
        workspace_board_section=unrelated_workspace_board_section,
        title="I am an unrelated task",
    )


@pytest.fixture
def label(
    faker: Faker, workspace: models.Workspace, workspace_user: WorkspaceUser
) -> models.Label:
    """Return a label."""
    return label_create(
        workspace=workspace,
        name=faker.catch_phrase(),
        who=workspace_user.user,
        color=faker.pyint(min_value=0, max_value=6),
    )


@pytest.fixture
def unrelated_label(
    faker: Faker,
    unrelated_workspace: models.Workspace,
    unrelated_workspace_user: WorkspaceUser,
) -> models.Label:
    """Create an unrelated label."""
    return label_create(
        workspace=unrelated_workspace,
        name=faker.catch_phrase(),
        who=unrelated_workspace_user.user,
        color=faker.pyint(min_value=0, max_value=6),
    )


@pytest.fixture
def labels(workspace: Workspace, workspace_user: WorkspaceUser) -> list[Label]:
    """Create several sub tasks."""
    N = 5
    return [
        label_create(
            who=workspace_user.user,
            workspace=workspace,
            name=f"Label {i}",
            color=i,
        )
        for i in range(N)
    ]


@pytest.fixture
def task_label(task: models.Task, label: models.Label) -> models.TaskLabel:
    """Return a label."""
    # TODO we will use a task_add_label service here in the future
    return task.add_label(label)


@pytest.fixture
def sub_task(
    faker: Faker, task: models.Task, workspace_user: WorkspaceUser
) -> models.SubTask:
    """Return subtask."""
    return sub_task_create(
        who=workspace_user.user,
        task=task,
        title=faker.sentence(),
        description=faker.paragraph(),
        done=faker.pybool(),
    )


@pytest.fixture
def chat_message(
    task: models.Task,
    workspace_user: models.WorkspaceUser,
    faker: Faker,
) -> models.ChatMessage:
    """Return ChatMessage instance."""
    return chat_message_create(
        who=workspace_user.user,
        task=task,
        text=faker.paragraph(),
    )
