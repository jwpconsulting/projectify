"""Seeddb command."""
import random

from django.contrib import (
    auth,
)
from django.core.management.base import (
    BaseCommand,
)
from django.db import (
    transaction,
)

import tqdm
from user.factory import (
    SuperUserFactory,
    UserFactory,
)
from workspace.factory import (
    TaskFactory,
    WorkspaceBoardFactory,
    WorkspaceBoardSectionFactory,
    WorkspaceFactory,
)
from workspace.models import (
    Workspace,
    WorkspaceBoard,
)


class Command(BaseCommand):
    """Command."""

    N_USERS = 5

    def create_users(self):
        """Create users."""
        if auth.get_user_model().objects.count():
            return
        super_user = SuperUserFactory(
            email="admin@localhost",
            password="password",
        )
        guest_user = UserFactory(
            email="guest@localhost",
            password="password",
        )

        users = super_user, guest_user
        n_users = self.N_USERS - auth.get_user_model().objects.count()
        UserFactory.create_batch(n_users)
        users = list(auth.get_user_model().objects.all())
        return users

    N_WORKSPACES = 3
    N_WORKSPACE_BOARDS = 3
    SECTION_TITLES = [
        "Backlog",
        "To Do",
        "Ongoing",
        "Review",
        "Done",
    ]

    def populate_workspace_board(self, board):
        """Populate a workspace board."""
        if board.workspaceboardsection_set.count():
            return
        for title in tqdm.tqdm(
            self.SECTION_TITLES,
            desc="Workspace board sections",
        ):
            section = WorkspaceBoardSectionFactory(
                workspace_board=board,
                title=title,
            )
            for _ in tqdm.trange(10, desc="Tasks"):
                TaskFactory(workspace_board_section=section)

    def create_workspaces(self, users):
        """Create workspaces."""
        n_workspaces = self.N_WORKSPACES - Workspace.objects.count()
        for _ in tqdm.trange(n_workspaces, desc="Workspaces with users"):
            WorkspaceFactory(add_users=random.sample(users, 3))
        workspaces = Workspace.objects.all()
        for workspace in tqdm.tqdm(workspaces, desc="Workspaces"):
            n = self.N_WORKSPACE_BOARDS - workspace.workspaceboard_set.count()
            WorkspaceBoardFactory.create_batch(
                n,
                workspace=workspace,
            )
            boards = WorkspaceBoard.objects.all()
            for board in tqdm.tqdm(boards, desc="Workspace boards"):
                self.populate_workspace_board(board)

    @transaction.atomic
    def handle(self, *args, **options):
        """Handle."""
        users = self.create_users()
        self.create_workspaces(users)
