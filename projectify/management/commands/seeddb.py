"""
Seeddb command.

The various --n-* arguments can be used to ensure that the database contains at
least N of each object.

For workspaces that already exist, we don't touch them.

For new workspaces, we add quantities of objects, as specified in the arguments
"""
import random
from argparse import (
    ArgumentParser,
)
from collections.abc import (
    Sequence,
)
from typing import (
    Any,
    Optional,
)

from django.contrib import (
    auth,
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
from user.factory import (
    SuperUserFactory,
    UserFactory,
)
from workspace.factory import (
    ChatMessageFactory,
    LabelFactory,
    SubTaskFactory,
    TaskFactory,
    WorkspaceBoardFactory,
    WorkspaceBoardSectionFactory,
    WorkspaceFactory,
)
from workspace.models import (
    Label,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
)


class Command(BaseCommand):
    """Command."""

    def create_users(
        self, n_users: int
    ) -> Optional[Sequence[AbstractBaseUser]]:
        """Create users."""
        User = auth.get_user_model()
        existing_users = User.objects.count()
        if existing_users == 0:
            SuperUserFactory.create(
                email="admin@localhost",
                password="password",
            )
            self.stdout.write("Created super_user")
            UserFactory.create(
                email="guest@localhost",
                password="password",
            )
            self.stdout.write("Created guest_user")
        remaining_users = n_users - User.objects.count()
        new_users = UserFactory.create_batch(remaining_users)
        self.stdout.write(f"Created {len(new_users)} remaining users")
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
        section: WorkspaceBoardSection,
        labels: Sequence[Label],
        n_tasks: int,
    ) -> None:
        """Create tasks for a workspace board section."""
        for _ in range(n_tasks):
            task = TaskFactory.create(workspace_board_section=section)
            n_labels = random.randint(0, 3)
            chosen_labels = random.choices(labels, k=n_labels)
            for label in chosen_labels:
                task.add_label(label)
            self.stdout.write(f"Assigned {n_labels} labels to task {task}")
            n_sub_tasks = random.randint(0, 3)
            for _ in range(n_sub_tasks):
                SubTaskFactory(task=task)
            self.stdout.write(f"Created {n_sub_tasks} sub tasks")
            n_chat_messages = random.randint(0, 3)
            for _ in range(n_chat_messages):
                ChatMessageFactory(task=task)
            self.stdout.write(f"Created {n_chat_messages} chat messages")
        self.stdout.write(f"Created {n_tasks} tasks")

    def create_workspace_board(
        self, workspace: Workspace, labels: Sequence[Label], n_tasks: int
    ) -> WorkspaceBoard:
        """Populate a workspace board."""
        board = WorkspaceBoardFactory.create(workspace=workspace)
        for title in self.SECTION_TITLES:
            section = WorkspaceBoardSectionFactory.create(
                workspace_board=board,
                title=title,
            )
            self.create_tasks(
                section, labels, random.randint(n_tasks // 2, n_tasks)
            )
        self.stdout.write(
            f"Created {len(self.SECTION_TITLES)} workspace board sections"
        )
        return board

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
        remaining_workspaces = n_workspaces - Workspace.objects.count()
        workspaces = [
            WorkspaceFactory.create(
                add_users=random.sample(users, n_add_users)
            )
            for _ in range(remaining_workspaces)
        ]
        self.stdout.write(
            f"Created {remaining_workspaces} remaining workspaces"
        )

        for workspace in workspaces:
            labels = LabelFactory.create_batch(
                n_labels,
                workspace=workspace,
            )
            self.stdout.write(f"Created {n_labels} labels")
            for _ in range(n_workspace_boards):
                self.create_workspace_board(workspace, labels, n_tasks)
            self.stdout.write(f"Created {n_workspace_boards} workspace boards")
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
