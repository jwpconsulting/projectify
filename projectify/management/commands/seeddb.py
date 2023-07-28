"""Seeddb command."""
import random
from argparse import (
    ArgumentParser,
)
from typing import (
    Any,
    Iterable,
    Optional,
    Sequence,
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

import tqdm
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
        if auth.get_user_model().objects.count():
            return None
        super_user = SuperUserFactory.create(
            email="admin@localhost",
            password="password",
        )
        guest_user = UserFactory.create(
            email="guest@localhost",
            password="password",
        )

        users: Iterable[AbstractBaseUser] = super_user, guest_user
        remaining_users = n_users - auth.get_user_model().objects.count()
        UserFactory.create_batch(remaining_users)
        users = list(auth.get_user_model().objects.all())
        return users

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
        for _ in tqdm.trange(n_tasks, desc="Tasks"):
            task = TaskFactory.create(workspace_board_section=section)
            n_labels = random.randint(0, 3)
            chosen_labels = random.choices(labels, k=n_labels)
            for label in tqdm.tqdm(chosen_labels, desc="Labels"):
                task.add_label(label)
            for _ in tqdm.trange(3, desc="Subtasks & chat messages"):
                SubTaskFactory(task=task)
                ChatMessageFactory(task=task)

    def populate_workspace_board(
        self, board: WorkspaceBoard, n_tasks: int
    ) -> None:
        """Populate a workspace board."""
        labels = list(board.workspace.label_set.all())
        if board.workspaceboardsection_set.count():
            return None
        for title in tqdm.tqdm(
            self.SECTION_TITLES,
            desc="Workspace board sections",
        ):
            section = WorkspaceBoardSectionFactory.create(
                workspace_board=board,
                title=title,
            )
            self.create_tasks(section, labels, n_tasks)

    def create_workspaces(
        self,
        users: Sequence[AbstractBaseUser],
        n_workspaces: int,
        n_workspace_boards: int,
        n_labels: int,
        n_tasks: int,
        n_add_users: int,
    ) -> Iterable[Workspace]:
        """Create workspaces."""
        remaining_workspaces = n_workspaces - Workspace.objects.count()
        for _ in tqdm.trange(
            remaining_workspaces, desc="Workspaces with users"
        ):
            WorkspaceFactory(add_users=random.sample(users, n_add_users))
        workspaces = Workspace.objects.all()
        for workspace in tqdm.tqdm(workspaces, desc="Workspaces"):
            n_labels_create = n_labels - workspace.label_set.count()
            LabelFactory.create_batch(
                n_labels_create,
                workspace=workspace,
            )
            n = n_workspace_boards - workspace.workspaceboard_set.count()
            WorkspaceBoardFactory.create_batch(
                n,
                workspace=workspace,
            )
            boards = WorkspaceBoard.objects.all()
            for board in tqdm.tqdm(boards, desc="Workspace boards"):
                self.populate_workspace_board(board, n_tasks)
        return list(Workspace.objects.all())

    def create_corporate_accounts(
        self, workspaces: Iterable[Workspace]
    ) -> None:
        """Create corporate accounts."""
        for workspace in tqdm.tqdm(workspaces, desc="Corporate accounts"):
            if not hasattr(workspace, "customer"):
                CustomerFactory(
                    workspace=workspace,
                    subscription_status=CustomerSubscriptionStatus.ACTIVE,
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
            help="Ensure N workspaces are created",
        )
        parser.add_argument(
            "--n-workspace-boards",
            type=int,
            default=3,
            help="Ensure N workspace boards are created",
        )
        parser.add_argument(
            "--n-add-users",
            type=int,
            default=3,
            help="Ensure N users are added",
        )
        parser.add_argument(
            "--n-labels",
            type=int,
            default=3,
            help="Ensure N labels are added to a workspace",
        )
        parser.add_argument(
            "--n-tasks",
            type=int,
            default=10,
            help="Ensure N tasks are added to a workspace board",
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
        users = self.create_users(n_users)
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
