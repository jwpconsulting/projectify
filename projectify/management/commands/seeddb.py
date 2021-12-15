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
    WorkspaceBoardFactory,
    WorkspaceFactory,
)
from workspace.models import (
    Workspace,
)


class Command(BaseCommand):
    """Command."""

    USERS = 5

    def create_users(self):
        """Create users."""
        super_user = SuperUserFactory(
            email="admin@localhost",
            password="password",
        )
        guest_user = UserFactory(
            email="guest@localhost",
            password="password",
        )

        users = super_user, guest_user
        n_users = self.USERS - auth.get_user_model().objects.count()
        UserFactory.create_batch(n_users)
        users = list(auth.get_user_model().objects.all())

        return users

    N_WORKSPACES = 3
    N_WORKSPACE_BOARDS = 3

    def create_workspaces(self, users):
        """Create workspaces."""
        n_workspaces = self.N_WORKSPACES - Workspace.objects.count()
        for _ in tqdm.trange(n_workspaces, desc="Workspaces"):
            WorkspaceFactory(add_users=random.sample(users, 3))
        workspaces = Workspace.objects.all()
        for workspace in tqdm.tqdm(workspaces, desc="Workspace boards"):
            n = self.N_WORKSPACE_BOARDS - workspace.workspaceboard_set.count()
            WorkspaceBoardFactory.create_batch(n, workspace=workspace)

    @transaction.atomic
    def handle(self, *args, **options):
        """Handle."""
        users = self.create_users()
        self.create_workspaces(users)
