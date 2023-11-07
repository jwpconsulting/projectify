"""
Seeddb command.

The various --n-* arguments can be used to ensure that the database contains at
least N of each object.

For workspaces that already exist, we don't touch them.

For new workspaces, we add quantities of objects, as specified in the arguments

Assuming your development database is called projectify, you can do a full test
run by running
dropdb projectify && \
    createdb projectify && \
    poetry run ./manage.py migrate && \
    poetry run ./manage.py seeddb
"""
import random
from argparse import (
    ArgumentParser,
)
from collections.abc import (
    Mapping,
    Sequence,
)
from datetime import (
    timezone,
)
from itertools import (
    count,
    groupby,
)
from typing import (
    Any,
    Optional,
    TypedDict,
)
from uuid import (
    UUID,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.core.management.base import (
    BaseCommand,
)
from django.db import (
    transaction,
)

from corporate.factory import (
    CustomerFactory,
)
from corporate.models import (
    CustomerSubscriptionStatus,
)
from faker import (
    Faker,
)
from user.models import (
    User,
)
from workspace.models import (
    ChatMessage,
    Label,
    Task,
    TaskLabel,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
)
from workspace.models.sub_task import (
    SubTask,
)
from workspace.models.workspace_user import (
    WorkspaceUser,
)


class Command(BaseCommand):
    """Command."""

    fake: Faker

    def create_users(self, n_users: int) -> Optional[Sequence["User"]]:
        """Create users."""
        existing_users = User.objects.count()
        if existing_users == 0:
            User.objects.create_superuser(
                email="admin@localhost",
                password="password",
            )
            self.stdout.write("Created superuser")
            User.objects.create_user(
                email="guest@localhost",
                password="password",
            )
            self.stdout.write("Created normal user")
        remaining_users = n_users - User.objects.count()
        new_users = [
            User.objects.create_user(
                email=self.fake.email(),
            )
            for _ in range(remaining_users)
        ]
        self.stdout.write(f"Created {len(new_users)} new users")
        return list(User.objects.all())

    SECTION_TITLES = [
        "Backlog",
        "To Do",
        "Ongoing",
        "Review",
        "Done",
    ]

    def create_tasks(
        self,
        number: "count[int]",
        workspace: Workspace,
        workspace_board_sections: Sequence[WorkspaceBoardSection],
        labels: Sequence[Label],
        workspace_users: Sequence[WorkspaceUser],
        n_tasks: int,
    ) -> None:
        """Create tasks for a sequence workspace board sections."""
        tasks = Task.objects.bulk_create(
            [
                Task(
                    title=self.fake.word(),
                    description=self.fake.paragraph(),
                    workspace_board_section=workspace_board_section,
                    deadline=self.fake.date_time(tzinfo=timezone.utc),
                    workspace=workspace,
                    _order=_order,
                    number=next(number),
                    assignee=random.choice(workspace_users),
                )
                for workspace_board_section in workspace_board_sections
                for _order in range(random.randint(n_tasks // 2, n_tasks))
            ]
        )
        self.stdout.write(f"Created {len(tasks)} tasks")

        task_labels = TaskLabel.objects.bulk_create(
            [
                TaskLabel(
                    task=task,
                    label=label,
                )
                for task in tasks
                for label in random.sample(
                    # Make sure we don't go over the amount of labels we have
                    # actually created for this workspace
                    labels,
                    min(len(labels), random.randint(0, 3)),
                )
            ]
        )
        self.stdout.write(f"Created {len(task_labels)} task labels")

        sub_tasks = SubTask.objects.bulk_create(
            [
                SubTask(
                    title=self.fake.word(),
                    description=self.fake.paragraph(),
                    task=task,
                    done=self.fake.pybool(),
                    _order=_order,
                )
                for task in tasks
                for _order in range(random.randint(0, 3))
            ]
        )
        self.stdout.write(f"Created {len(sub_tasks)} sub tasks")

        chat_messages = ChatMessage.objects.bulk_create(
            [
                ChatMessage(
                    task=task,
                    text=self.fake.paragraph(),
                    author=random.choice(workspace_users),
                )
                for task in tasks
                for _ in range(random.randint(0, 3))
            ]
        )
        self.stdout.write(f"Created {len(chat_messages)} chat messages")
        self.stdout.write(f"Populated {len(tasks)} tasks")

    def populate_workspace_boards(
        self,
        number: "count[int]",
        workspace: Workspace,
        workspace_boards: Sequence[WorkspaceBoard],
        workspace_users: Sequence[WorkspaceUser],
        labels: Sequence[Label],
        n_tasks: int,
    ) -> None:
        """Populate a workspace board."""
        workspace_board_sections = WorkspaceBoardSection.objects.bulk_create(
            [
                WorkspaceBoardSection(
                    workspace_board=workspace_board,
                    title=title,
                    _order=_order,
                )
                for workspace_board in workspace_boards
                for _order, title in enumerate(self.SECTION_TITLES)
            ]
        )
        self.stdout.write(
            f"Created {len(self.SECTION_TITLES)} workspace board sections"
        )
        self.create_tasks(
            number,
            workspace,
            workspace_board_sections,
            labels,
            workspace_users,
            n_tasks,
        )
        self.stdout.write(
            f"Populated {len(self.SECTION_TITLES)} workspace board sections"
        )

    def create_workspaces(
        self,
        users: Sequence[AbstractBaseUser],
        n_workspaces: int,
        n_workspace_boards: int,
        n_labels: int,
        n_tasks: int,
        n_add_users: int,
    ) -> Sequence[Workspace]:
        """Create workspaces."""
        existing_workspaces = Workspace.objects.count()
        self.stdout.write(
            f"There are already {existing_workspaces} workspaces"
        )
        remaining_workspaces = max(0, n_workspaces - existing_workspaces)

        workspaces: list[Workspace] = Workspace.objects.bulk_create(
            [
                Workspace(
                    title=self.fake.word(),
                    description=self.fake.paragraph(),
                )
                for _ in range(remaining_workspaces)
            ]
        )
        self.stdout.write(f"Created {len(workspaces)} new workspaces")

        workspaces_workspace_users = WorkspaceUser.objects.bulk_create(
            [
                WorkspaceUser(
                    workspace=workspace,
                    user=user,
                )
                for workspace in workspaces
                for user in random.sample(users, n_add_users)
            ]
        )
        self.stdout.write(
            f"Added {len(workspaces_workspace_users)} users to "
            f"{len(workspaces)} new workspaces"
        )
        workspaces_labels = Label.objects.bulk_create(
            [
                Label(
                    name=self.fake.catch_phrase(),
                    color=random.randint(0, 6),
                    workspace=workspace,
                )
                for workspace in workspaces
                for _ in range(n_labels)
            ]
        )
        self.stdout.write(f"Created {len(workspaces_labels)} labels")

        workspaces_workspace_boards = WorkspaceBoard.objects.bulk_create(
            [
                WorkspaceBoard(
                    title=self.fake.word(),
                    description=self.fake.paragraph(),
                    workspace=workspace,
                    deadline=self.fake.date_time(tzinfo=timezone.utc),
                )
                for workspace in workspaces
                for _ in range(n_workspace_boards)
            ]
        )
        self.stdout.write(
            f"Created {len(workspaces_workspace_boards)} workspace boards"
        )

        # The idea here is that instead of going into each nested object in
        # a for loop, we create them altogether at once.
        # So:
        # Create all workspaces
        # Assign all users to all new workspaces
        # Create all labels for all new workspaces
        # Create all workspace boards for all new workspaces
        # etc.
        Altogether = TypedDict(
            "Altogether",
            {
                "workspace": Workspace,
                "workspace_users": list[WorkspaceUser],
                "labels": list[Label],
                "workspace_boards": list[WorkspaceBoard],
            },
        )
        altogether: Mapping[UUID, Altogether] = {
            workspace.uuid: {
                "workspace": workspace,
                "workspace_users": list(workspace_users),
                "labels": list(labels),
                "workspace_boards": list(workspace_boards),
            }
            for (
                (workspace, workspace_users),
                (_, labels),
                (_, workspace_boards),
            ) in zip(
                groupby(workspaces_workspace_users, key=lambda u: u.workspace),
                groupby(workspaces_labels, key=lambda l: l.workspace),
                groupby(
                    workspaces_workspace_boards, key=lambda b: b.workspace
                ),
            )
        }

        for together in altogether.values():
            number = count()
            self.populate_workspace_boards(
                number,
                together["workspace"],
                together["workspace_boards"],
                list(together["workspace_users"]),
                list(together["labels"]),
                n_tasks,
            )
            together["workspace"].highest_task_number = next(number)
            together["workspace"].save()
            self.stdout.write(
                f'Populated {len(together["workspace_boards"])} workspace '
                f"boards"
            )
        return workspaces

    def create_corporate_accounts(
        self, workspaces: Sequence[Workspace]
    ) -> None:
        """Create corporate accounts."""
        for workspace in workspaces:
            if not hasattr(workspace, "customer"):
                CustomerFactory(
                    workspace=workspace,
                    subscription_status=CustomerSubscriptionStatus.ACTIVE,
                )
        self.stdout.write(
            f"Created customers for {len(workspaces)} workspaces"
        )

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add arguments."""
        parser.add_argument(
            "--n-users",
            type=int,
            default=40,
            help="Ensure N users are created",
        )
        parser.add_argument(
            "--n-workspaces",
            type=int,
            default=15,
            help="Ensure N workspaces are present",
        )
        parser.add_argument(
            "--n-workspace-boards",
            type=int,
            default=20,
            help="Ensure N workspace boards are added to a new workspace",
        )
        parser.add_argument(
            "--n-add-users",
            type=int,
            default=15,
            help="Ensure N users are added to new workspaces",
        )
        parser.add_argument(
            "--n-labels",
            type=int,
            default=20,
            help="Ensure N labels are added to a new workspace",
        )
        parser.add_argument(
            "--n-tasks",
            type=int,
            default=40,
            help="Ensure up to N tasks are in new workspace board section",
        )

    @transaction.atomic
    def handle(self, *args: object, **options: Any) -> None:
        """Handle."""
        self.fake = Faker()
        n_users: int = options["n_users"]
        n_workspaces: int = options["n_workspaces"]
        n_workspace_boards: int = options["n_workspace_boards"]
        n_labels: int = options["n_labels"]
        n_tasks: int = options["n_tasks"]
        n_add_users: int = options["n_add_users"]
        if n_add_users > n_users:
            self.stdout.write(
                f"You are trying to add more users to each workspace "
                f"({n_add_users} users) than are "
                f"requested to be created in the first place. "
                f"({n_users} users) "
                f"The amount of users created will be increase to "
                f"{n_add_users}."
            )
        users = self.create_users(max(n_users, n_add_users))
        if not users:
            return
        workspaces = self.create_workspaces(
            users,
            n_workspaces=n_workspaces,
            n_workspace_boards=n_workspace_boards,
            n_labels=n_labels,
            n_add_users=n_add_users,
            n_tasks=n_tasks,
        )
        self.create_corporate_accounts(workspaces)
