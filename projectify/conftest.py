# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""
conftest.py contains top level and workspace app fixtures.

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

import base64
import random
from datetime import datetime
from datetime import timezone as dt_timezone

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import client
from django.utils import timezone

import pytest
from faker import Faker
from rest_framework.test import APIClient

from projectify.corporate.models import Coupon, Customer
from projectify.corporate.services.coupon import coupon_create
from projectify.corporate.services.stripe import (
    customer_activate_subscription,
    customer_cancel_subscription,
)
from projectify.user import models as user_models
from projectify.user.models import User
from projectify.user.services.internal import (
    user_create,
    user_create_superuser,
)
from projectify.user.services.user_invite import (
    user_invite_create,
    user_invite_redeem,
)
from projectify.workspace.models import (
    ChatMessage,
    Label,
    Project,
    Section,
    SubTask,
    Task,
    TaskLabel,
    TeamMember,
    TeamMemberInvite,
    TeamMemberRoles,
    Workspace,
)
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


@pytest.fixture
def password(faker: Faker) -> str:
    """Set default password."""
    pw: str = faker.password(length=20)
    return pw


@pytest.fixture
def user(faker: Faker, password: str) -> user_models.User:
    """Return a db user."""
    user = user_create(email=faker.email(), password=password)
    user.is_active = True
    user.preferred_name = faker.name()
    user.save()
    return user


@pytest.fixture
def superuser(faker: Faker) -> user_models.User:
    """Return a db super user."""
    return user_create_superuser(email=faker.email())


@pytest.fixture
def other_user(faker: Faker) -> user_models.User:
    """Return another db user."""
    return user_create(email=faker.email())


@pytest.fixture
def unrelated_user(faker: Faker) -> user_models.User:
    """Return unrelated user normally not in the same workspace."""
    return user_create(email=faker.email())


@pytest.fixture
def meddling_user(faker: Faker, password: str) -> user_models.User:
    """Create a canary user to check permissions."""
    user = user_create(email=faker.email(), password=password)
    user.is_active = True
    user.preferred_name = faker.name()
    user.save()
    return user


@pytest.fixture
def inactive_user(faker: Faker, password: str) -> user_models.User:
    """Return an inactive db user."""
    return user_create(email=faker.email(), password=password)


@pytest.fixture
def user_invite(faker: Faker) -> user_models.UserInvite:
    """Return a user invite."""
    user_invite = user_invite_create(email=faker.email())
    if user_invite is None:
        raise ValueError("Expected user_invite")
    return user_invite


@pytest.fixture
def redeemed_user_invite(faker: Faker) -> user_models.UserInvite:
    """Return a redeemed user invite."""
    email = faker.email()
    user_invite = user_invite_create(email=email)
    if user_invite is None:
        raise AssertionError("Expected user_invite")
    user = user_create(email=email)
    user_invite_redeem(user=user, user_invite=user_invite)
    return user_invite


@pytest.fixture
def user_client(client: client.Client, user: User) -> client.Client:
    """Return logged in client."""
    client.force_login(user)
    return client


@pytest.fixture
def superuser_client(client: client.Client, superuser: User) -> client.Client:
    """Return logged in super user client."""
    client.force_login(superuser)
    return client


@pytest.fixture
def rest_client() -> APIClient:
    """Return a logged-out client to test DRF views."""
    return APIClient()


@pytest.fixture
def rest_user_client(user: User) -> APIClient:
    """Return a logged in client that we can use to test DRF views."""
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def rest_meddling_client(meddling_user: User) -> APIClient:
    """Return a test client to check third party logged in access."""
    client = APIClient()
    client.force_authenticate(meddling_user)
    return client


@pytest.fixture
def png_image() -> bytes:
    """Return a simple png file."""
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgAgAAAAAcoT2JAAAABGdBTUEAAYagMeiWX\
        wAAAB9JREFUeJxjYAhd9R+M8TCIUMIAU4aPATMJH2OQuQcAvUl/gYsJiakAAAAASUVORK5\
        CYII="
    )


@pytest.fixture
def uploaded_file(png_image: bytes) -> SimpleUploadedFile:
    """Return an UploadFile instance of the above png file."""
    return SimpleUploadedFile("test.png", png_image)


@pytest.fixture(scope="session", autouse=True)
def faker_seed() -> int:
    """Return a random seed every session."""
    return random.randint(0, 2**16)


@pytest.fixture
def now() -> datetime:
    """Return now."""
    return timezone.now()


@pytest.fixture
def workspace(faker: Faker, user: User) -> Workspace:
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
    return timezone.now()


@pytest.fixture
def other_workspace(user: User) -> Workspace:
    """Return workspace."""
    workspace = workspace_create(
        title="Other workspace",
        description="This is another workspace that the current user can access",
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
def unrelated_workspace(faker: Faker, unrelated_user: User) -> Workspace:
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
    workspace: Workspace, team_member: TeamMember, faker: Faker
) -> TeamMemberInvite:
    """Return team member invite."""
    email: str = faker.email()
    invite = team_member_invite_create(
        who=team_member.user, workspace=workspace, email_or_user=email
    )
    assert isinstance(invite, TeamMemberInvite)
    return invite


@pytest.fixture
def team_member(workspace: Workspace, user: User) -> TeamMember:
    """Return team member with owner status."""
    team_member = team_member_find_for_workspace(
        workspace=workspace, user=user
    )
    assert team_member
    return team_member


@pytest.fixture
def other_team_member(workspace: Workspace, other_user: User) -> TeamMember:
    """Return team member for other_user."""
    team_member = workspace_add_user(
        workspace=workspace,
        user=other_user,
        role=TeamMemberRoles.OWNER,
    )
    assert team_member
    return team_member


@pytest.fixture
def unrelated_team_member(
    unrelated_workspace: Workspace, unrelated_user: User
) -> TeamMember:
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
    workspace: Workspace,
) -> Project:
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
def other_project_same_workspace(user: User, workspace: Workspace) -> Project:
    """Return project that belongs to the normal workspace."""
    return project_create(
        who=user,
        title="Other project for the same workspace",
        description="This is another project that this user can access",
        workspace=workspace,
        due_date=None,
    )


@pytest.fixture
def other_project(user: User, other_workspace: Workspace) -> Project:
    """
    Return project that belongs to the other workspace.

    The normal fixture user can still access this.
    """
    return project_create(
        who=user,
        title="Other project from a different workspace",
        description="This is in another workspace and the user can access it",
        workspace=other_workspace,
        due_date=None,
    )


@pytest.fixture
def unrelated_project(
    unrelated_team_member: TeamMember,
    faker: Faker,
    unrelated_workspace: Workspace,
) -> Project:
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
    workspace: Workspace,
    other_team_member: TeamMember,
    faker: Faker,
) -> Project:
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
    project: Project,
    # Another team member creates it, so that we can correctly assess
    # permissions and not implicitly associate the main user with this
    # workspace
    other_team_member: TeamMember,
    faker: Faker,
) -> Section:
    """Return section."""
    return section_create(
        who=other_team_member.user,
        project=project,
        title=faker.sentence(),
    )


@pytest.fixture
def other_section(
    project: Project,
    team_member: TeamMember,
    faker: Faker,
) -> Section:
    """Create another section."""
    return section_create(
        who=team_member.user,
        project=project,
        title=faker.sentence(),
    )


@pytest.fixture
def other_other_section(
    project: Project,
    team_member: TeamMember,
    faker: Faker,
) -> Section:
    """Create yet another section."""
    return section_create(
        who=team_member.user,
        project=project,
        title=faker.sentence(),
    )


@pytest.fixture
def unrelated_section(
    unrelated_project: Project,
    unrelated_team_member: TeamMember,
    faker: Faker,
) -> Section:
    """Return unrelated section."""
    return section_create(
        who=unrelated_team_member.user,
        project=unrelated_project,
        title=faker.sentence(),
    )


@pytest.fixture
def task(
    section: Section,
    team_member: TeamMember,
    faker: Faker,
) -> Task:
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
def other_task(task: Task, section: Section, team_member: TeamMember) -> Task:
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
    unrelated_section: Section,
    unrelated_team_member: TeamMember,
) -> Task:
    """Return another task belonging to the same section."""
    return task_create(
        who=unrelated_team_member.user,
        section=unrelated_section,
        title="I am an unrelated task",
    )


@pytest.fixture
def label(
    faker: Faker, workspace: Workspace, team_member: TeamMember
) -> Label:
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
    unrelated_workspace: Workspace,
    unrelated_team_member: TeamMember,
) -> Label:
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
def task_label(task: Task, label: Label) -> TaskLabel:
    """Return a label."""
    # TODO we will use a task_add_label service here in the future
    task.labels.add(label)
    return TaskLabel.objects.get(task=task)


@pytest.fixture
def sub_task(faker: Faker, task: Task, team_member: TeamMember) -> SubTask:
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
    task: Task,
    team_member: TeamMember,
    faker: Faker,
) -> ChatMessage:
    """Return ChatMessage instance."""
    return chat_message_create(
        who=team_member.user, task=task, text=faker.paragraph()
    )


@pytest.fixture
def stripe_publishable_key(faker: Faker) -> str:
    """Return a convincing looking stripe publishable key."""
    key: str = faker.hexify(
        "pk_test_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def stripe_secret_key(faker: Faker) -> str:
    """Return a convincing looking stripe secret key."""
    key: str = faker.hexify(
        "sk_test_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def stripe_price_object(faker: Faker) -> str:
    """Return a convincing looking stripe price object."""
    key: str = faker.hexify("price_^^^^^^^^^^^^^^^^^^^^^^^^")
    return key


@pytest.fixture
def stripe_endpoint_secret(faker: Faker) -> str:
    """Return a convincing looking stripe endpoint secret."""
    key: str = faker.hexify(
        "whsec_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def unpaid_customer(workspace: Workspace) -> Customer:
    """Create customer."""
    customer_cancel_subscription(customer=workspace.customer)
    # Workaround, since activating a subscription sets the stripe customer id
    workspace.customer.stripe_customer_id = None
    workspace.customer.save()
    return workspace.customer


@pytest.fixture
def stripe_customer_id(faker: Faker) -> str:
    """Return a convincing stripe customer id."""
    stripe_customer_id: str = faker.bothify("stripe_###???###")
    return stripe_customer_id


@pytest.fixture
def paid_customer(
    unpaid_customer: Customer, stripe_customer_id: str
) -> Customer:
    """Create customer."""
    customer_activate_subscription(
        customer=unpaid_customer,
        stripe_customer_id=stripe_customer_id,
        seats=1337,
    )
    return unpaid_customer


@pytest.fixture
def coupon(superuser: User) -> Coupon:
    """Create a working coupon."""
    return coupon_create(who=superuser, seats=20, prefix="i-am-a-test-coupon")
