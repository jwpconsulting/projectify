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
    Sequence,
)
from datetime import (
    timezone,
)
from itertools import (
    count,
)
from typing import (
    Any,
    Optional,
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
        self.stdout.write(f"Created {len(new_users)} remaining users")
        return list(User.objects.all())

    SECTION_TITLES = [
        "Backlog",
        "To Do",
        "Ongoing",
        "Review",
        "Done",
    ]

    # TODO We can collect all workspace boards etc bottom-up and then
    # bulk create all tasks at once. That might be much faster.
    def create_tasks(
        self,
        number: "count[int]",
        section: WorkspaceBoardSection,
        labels: Sequence[Label],
        workspace_users: Sequence[WorkspaceUser],
        n_tasks: int,
    ) -> None:
        """Create tasks for a workspace board section."""
        workspace = section.workspace
        tasks = [
            Task(
                title=self.fake.word(),
                description=self.fake.paragraph(),
                workspace_board_section=section,
                deadline=self.fake.date_time(tzinfo=timezone.utc),
                workspace=workspace,
                _order=_order,
                number=next(number),
            )
            for _order in range(n_tasks)
        ]
        Task.objects.bulk_create(tasks)
        self.stdout.write(f"Created {n_tasks} tasks")
        for task in tasks:
            n_labels = random.randint(0, 3)
            chosen_labels = random.choices(labels, k=n_labels)
            for label in chosen_labels:
                task.add_label(label)
            self.stdout.write(f"Assigned {n_labels} labels to task {task}")
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
        self.stdout.write(f"Populated {n_tasks} tasks")

    def populate_workspace_board(
        self,
        number: "count[int]",
        workspace_board: WorkspaceBoard,
        workspace_users: Sequence[WorkspaceUser],
        labels: Sequence[Label],
        n_tasks: int,
    ) -> None:
        """Populate a workspace board."""
        sections = WorkspaceBoardSection.objects.bulk_create(
            [
                WorkspaceBoardSection(
                    workspace_board=workspace_board,
                    title=title,
                    _order=_order,
                )
                for _order, title in enumerate(self.SECTION_TITLES)
            ]
        )
        self.stdout.write(
            f"Created {len(self.SECTION_TITLES)} workspace board sections"
        )
        for section in sections:
            self.create_tasks(
                number,
                section,
                labels,
                workspace_users,
                random.randint(n_tasks // 2, n_tasks),
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
        self.stdout.write(f"Created {len(workspaces)} remaining workspaces")
        workspaces_workspace_users: list[list[WorkspaceUser]] = [
            WorkspaceUser.objects.bulk_create(
                [
                    WorkspaceUser(
                        workspace=workspace,
                        user=user,
                    )
                    for user in random.sample(users, n_add_users)
                ]
            )
            for workspace in workspaces
        ]
        self.stdout.write(
            f"Added users to {len(workspaces)} remaining workspaces"
        )

        for workspace, workspace_users in zip(
            workspaces, workspaces_workspace_users
        ):
            labels = Label.objects.bulk_create(
                [
                    Label(
                        name=self.fake.catch_phrase(),
                        color=random.randint(0, 6),
                        workspace=workspace,
                    )
                    for _ in range(n_labels)
                ]
            )
            self.stdout.write(f"Created {n_labels} labels")
            workspace_boards = WorkspaceBoard.objects.bulk_create(
                [
                    WorkspaceBoard(
                        title=self.fake.word(),
                        description=self.fake.paragraph(),
                        workspace=workspace,
                        deadline=self.fake.date_time(tzinfo=timezone.utc),
                    )
                    for _ in range(n_workspace_boards)
                ]
            )
            number = count()
            for workspace_board in workspace_boards:
                self.populate_workspace_board(
                    number, workspace_board, workspace_users, labels, n_tasks
                )
            self.stdout.write(
                f"Created {len(workspace_boards)} workspace boards"
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
            "--n-users", type=int, default=5, help="Ensure N users are created"
        )
        parser.add_argument(
            "--n-workspaces",
            type=int,
            default=5,
            help="Ensure N workspaces are present",
        )
        parser.add_argument(
            "--n-workspace-boards",
            type=int,
            default=3,
            help="Ensure N workspace boards are added to a new workspace",
        )
        parser.add_argument(
            "--n-add-users",
            type=int,
            default=3,
            help="Ensure N users are added to new workspaces",
        )
        parser.add_argument(
            "--n-labels",
            type=int,
            default=3,
            help="Ensure N labels are added to a new workspace",
        )
        parser.add_argument(
            "--n-tasks",
            type=int,
            default=10,
            help="Ensure N tasks are added to a new workspace board",
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
