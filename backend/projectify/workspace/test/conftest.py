# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
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

from datetime import datetime
from datetime import timezone as dt_timezone

from django.utils import timezone

import pytest
from faker import Faker

from projectify.corporate.services.stripe import customer_activate_subscription
from projectify.user.models import User, UserInvite
from projectify.workspace.models.label import Label
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.team_member_invite import TeamMemberInvite
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.selectors.team_member import (
    team_member_find_for_workspace,
)
from projectify.workspace.services.chat_message import chat_message_create
from projectify.workspace.services.label import label_create
from projectify.workspace.services.project import (
    project_archive,
    project_create,
)
from projectify.workspace.services.section import section_create
from projectify.workspace.services.sub_task import sub_task_create
from projectify.workspace.services.task import task_create
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
)
from projectify.workspace.services.workspace import (
    workspace_add_user,
    workspace_create,
)

from .. import models


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
    # Give ourselves some more seats so that tests can pass
    customer_activate_subscription(
        customer=customer, stripe_customer_id="stripe_", seats=10
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
        customer=customer,
        stripe_customer_id="stripe_",
        seats=10,
    )
    # TODO right now our tests depend on the workspace being paid for
    # We should also be able to test most actions here for a workspace that
    # isn't paid.
    return workspace


@pytest.fixture
def team_member_invite(
    workspace: models.Workspace,
    team_member: TeamMember,
    # TODO user_invite needed to redeem invite, right? verify.
    user_invite: UserInvite,
    faker: Faker,
) -> models.TeamMemberInvite:
    """Return team member invite."""
    email: str = faker.email()
    invite = team_member_invite_create(
        who=team_member.user, workspace=workspace, email_or_user=email
    )
    assert isinstance(invite, TeamMemberInvite)
    return invite


@pytest.fixture
def team_member(workspace: models.Workspace, user: User) -> models.TeamMember:
    """Return team member with owner status."""
    team_member = team_member_find_for_workspace(
        workspace=workspace, user=user
    )
    assert team_member
    return team_member


@pytest.fixture
def other_team_member(
    workspace: models.Workspace, other_user: User
) -> models.TeamMember:
    """Return team member for other_user."""
    team_member = workspace_add_user(
        workspace=workspace,
        user=other_user,
        role=models.TeamMemberRoles.OWNER,
    )
    assert team_member
    return team_member


@pytest.fixture
def unrelated_team_member(
    unrelated_workspace: models.Workspace, unrelated_user: User
) -> models.TeamMember:
    """Return team member for other_user."""
    team_member = team_member_find_for_workspace(
        workspace=unrelated_workspace, user=unrelated_user
    )
    assert team_member
    return team_member


@pytest.fixture
def project(
    other_team_member: TeamMember,
    faker: Faker,
    workspace: models.Workspace,
) -> models.Project:
    """Return project."""
    return project_create(
        who=other_team_member.user,
        title=faker.text(),
        description=faker.paragraph(),
        workspace=workspace,
        due_date=faker.date_time(tzinfo=dt_timezone.utc)
        if faker.pybool()
        else None,
    )


@pytest.fixture
def unrelated_project(
    unrelated_team_member: TeamMember,
    faker: Faker,
    unrelated_workspace: models.Workspace,
) -> models.Project:
    """Return an unrelated project."""
    return project_create(
        who=unrelated_team_member.user,
        title=faker.text(),
        description=faker.paragraph(),
        workspace=unrelated_workspace,
        # XXX another victim to non-determinism
        due_date=faker.date_time(tzinfo=dt_timezone.utc),
    )


@pytest.fixture
def archived_project(
    workspace: models.Workspace,
    other_team_member: TeamMember,
    faker: Faker,
) -> models.Project:
    """Return archived project."""
    project = project_create(
        who=other_team_member.user,
        title=faker.text(),
        description=faker.paragraph(),
        workspace=workspace,
    )
    project_archive(
        who=other_team_member.user,
        project=project,
        archived=True,
    )
    return project


@pytest.fixture
def section(
    project: models.Project,
    # Another team member creates it, so that we can correctly assess
    # permissions and not implicitly associate the main user with this
    # workspace
    other_team_member: TeamMember,
    faker: Faker,
) -> models.Section:
    """Return section."""
    return section_create(
        who=other_team_member.user,
        project=project,
        title=faker.sentence(),
    )


@pytest.fixture
def other_section(
    project: models.Project,
    team_member: TeamMember,
    faker: Faker,
) -> models.Section:
    """Create another section."""
    return section_create(
        who=team_member.user,
        project=project,
        title=faker.sentence(),
    )


@pytest.fixture
def other_other_section(
    project: models.Project,
    team_member: TeamMember,
    faker: Faker,
) -> models.Section:
    """Create yet another section."""
    return section_create(
        who=team_member.user,
        project=project,
        title=faker.sentence(),
    )


@pytest.fixture
def unrelated_section(
    unrelated_project: models.Project,
    unrelated_team_member: TeamMember,
    faker: Faker,
) -> models.Section:
    """Return unrelated section."""
    return section_create(
        who=unrelated_team_member.user,
        project=unrelated_project,
        title=faker.sentence(),
    )


@pytest.fixture
def task(
    section: models.Section,
    team_member: models.TeamMember,
    faker: Faker,
) -> models.Task:
    """Return task."""
    return task_create(
        who=team_member.user,
        section=section,
        title=faker.sentence(),
        description=faker.paragraph(),
        assignee=team_member if faker.pybool() else None,
        due_date=faker.date_time(tzinfo=dt_timezone.utc),
    )


@pytest.fixture
def other_task(
    task: models.Task, section: models.Section, team_member: models.TeamMember
) -> models.Task:
    """Return another task belonging to the same section."""
    # Make sure that this is created AFTER `task`
    del task
    return task_create(
        who=team_member.user,
        section=section,
        title="I am the other task",
    )


@pytest.fixture
def unrelated_task(
    unrelated_section: models.Section,
    unrelated_team_member: models.TeamMember,
) -> models.Task:
    """Return another task belonging to the same section."""
    return task_create(
        who=unrelated_team_member.user,
        section=unrelated_section,
        title="I am an unrelated task",
    )


@pytest.fixture
def label(
    faker: Faker, workspace: models.Workspace, team_member: TeamMember
) -> models.Label:
    """Return a label."""
    return label_create(
        workspace=workspace,
        name=faker.catch_phrase(),
        who=team_member.user,
        color=faker.pyint(min_value=0, max_value=6),
    )


@pytest.fixture
def unrelated_label(
    faker: Faker,
    unrelated_workspace: models.Workspace,
    unrelated_team_member: TeamMember,
) -> models.Label:
    """Create an unrelated label."""
    return label_create(
        workspace=unrelated_workspace,
        name=faker.catch_phrase(),
        who=unrelated_team_member.user,
        color=faker.pyint(min_value=0, max_value=6),
    )


@pytest.fixture
def labels(workspace: Workspace, team_member: TeamMember) -> list[Label]:
    """Create several sub tasks."""
    N = 5
    return [
        label_create(
            who=team_member.user,
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
    task.labels.add(label)
    return models.TaskLabel.objects.get(task=task)


@pytest.fixture
def sub_task(
    faker: Faker, task: models.Task, team_member: TeamMember
) -> models.SubTask:
    """Return subtask."""
    return sub_task_create(
        who=team_member.user,
        task=task,
        title=faker.sentence(),
        description=faker.paragraph(),
        done=faker.pybool(),
    )


@pytest.fixture
def chat_message(
    task: models.Task,
    team_member: models.TeamMember,
    faker: Faker,
) -> models.ChatMessage:
    """Return ChatMessage instance."""
    return chat_message_create(
        who=team_member.user,
        task=task,
        text=faker.paragraph(),
    )
