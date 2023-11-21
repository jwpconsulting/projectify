"""Test WorkspaceUser model."""
from django.contrib.auth.models import (
    AbstractUser,
)

import pytest

from user.factory import (
    UserFactory,
)
from workspace.models.workspace import (
    Workspace,
)
from workspace.services.workspace import (
    workspace_add_user,
)

from ... import (
    models,
)
from ...models import (
    WorkspaceUser,
    WorkspaceUserRoles,
)


@pytest.mark.django_db
class TestWorkspaceUserManager:
    """Test workspace user manager."""

    def test_filter_by_workspace_pks(
        self, workspace_user: WorkspaceUser, workspace: models.Workspace
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = WorkspaceUser.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_user]

    def test_filter_by_user(
        self, workspace: Workspace, workspace_user: WorkspaceUser
    ) -> None:
        """Test filter_by_user."""
        assert (
            WorkspaceUser.objects.filter_by_user(workspace_user.user).count()
            == 1
        )
        unrelated = UserFactory.create()
        assert (
            WorkspaceUser.objects.filter_by_user(workspace_user.user).count()
            == 1
        )
        assert WorkspaceUser.objects.filter_by_user(unrelated).count() == 0
        workspace_add_user(workspace, unrelated)
        assert WorkspaceUser.objects.filter_by_user(unrelated).count() == 2

    def test_get_by_workspace_and_user(
        self,
        workspace: models.Workspace,
        user: AbstractUser,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test get_by_workspace_and_user."""
        assert (
            WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                user,
            )
            == workspace_user
        )


@pytest.mark.django_db
class TestWorkspaceUser:
    """Test WorkspaceUser."""

    def test_factory(self, workspace_user: WorkspaceUser) -> None:
        """Test that the default rule is observer."""
        assert workspace_user.role == WorkspaceUserRoles.OWNER

    def test_workspace(
        self, workspace: models.Workspace, workspace_user: WorkspaceUser
    ) -> None:
        """Test workspace property."""
        assert workspace_user.workspace == workspace

    def test_assign_role(self, workspace_user: WorkspaceUser) -> None:
        """Test assign_role."""
        workspace_user.assign_role(WorkspaceUserRoles.OWNER)
        workspace_user.refresh_from_db()
        assert workspace_user.role == WorkspaceUserRoles.OWNER
