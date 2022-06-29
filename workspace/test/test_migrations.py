"""Test migrations in workspace app."""
import pytest


@pytest.mark.django_db
class Test0043:
    """Test migration 0043."""

    def test(self, migrator, settings):
        """Test that assignee_workspace_user is populated correctly."""
        old_state = migrator.apply_initial_migration(
            ("workspace", "0042_task_assignee_workspace_user")
        )
        Workspace = old_state.apps.get_model("workspace", "Workspace")
        WorkspaceBoard = old_state.apps.get_model(
            "workspace", "WorkspaceBoard"
        )
        WorkspaceBoardSection = old_state.apps.get_model(
            "workspace", "WorkspaceBoardSection"
        )
        Task = old_state.apps.get_model("workspace", "Task")
        WorkspaceUser = old_state.apps.get_model("workspace", "WorkspaceUser")
        User = old_state.apps.get_model(settings.AUTH_USER_MODEL)
        workspace = Workspace.objects.create(
            title="",
            description="",
        )
        workspace_board = WorkspaceBoard.objects.create(
            title="",
            description="",
            workspace=workspace,
        )
        workspace_board_section = WorkspaceBoardSection.objects.create(
            title="",
            description="",
            workspace_board=workspace_board,
        )
        user = User.objects.create(
            email="hello@example.com",
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )
        WorkspaceUser.objects.create(
            user=user,
            workspace=workspace,
        )
        task = Task.objects.create(
            title="",
            description="",
            workspace_board_section=workspace_board_section,
            workspace=workspace,
            assignee=user,
            number=1,
        )

        # Create a task with user, but no workspace user
        other_user = User.objects.create(
            email="goodbye@example.com",
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )
        other_task = Task.objects.create(
            title="",
            description="",
            workspace_board_section=workspace_board_section,
            workspace=workspace,
            assignee=other_user,
            number=2,
        )

        new_state = migrator.apply_tested_migration(
            ("workspace", "0043_auto_20220629_0742")
        )
        Task = new_state.apps.get_model("workspace", "Task")
        task = Task.objects.get(pk=task.pk)
        other_task = Task.objects.get(pk=other_task.pk)
        assert task.assignee_workspace_user is not None
        assert task.assignee_workspace_user.user == task.assignee
        assert other_task.assignee_workspace_user is None
