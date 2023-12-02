"""Test workspace mutations."""
import pytest

from workspace.models.workspace_user_invite import (
    add_or_invite_workspace_user,
)
from workspace.services.workspace import workspace_add_user

from ... import (
    models,
)


@pytest.mark.django_db
class TestRemoveUserFromWorkspaceMutation:
    """Test RemoveUserFromWorkspaceMutation."""

    query = """
mutation RemoveUserFromWorkspace($uuid: UUID!, $email: String!) {
    removeUserFromWorkspace(input: {uuid: $uuid, email: $email}) {
        uuid
        userInvitations {
            email
        }
    }
}
"""

    # TODO: Check if this test is in view tests
    @pytest.mark.xfail
    def test_query(
        self,
        other_user,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        workspace_add_user(workspace=workspace, user=other_user)
        assert workspace.users.count() == 2
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": other_user.email,
            },
        )
        assert result == {
            "data": {
                "removeUserFromWorkspace": {
                    "uuid": str(workspace.uuid),
                    "userInvitations": [],
                },
            },
        }
        assert workspace.users.count() == 1

    # TODO: Check if this test is in view tests
    @pytest.mark.xfail
    def test_uninvite_on_invite(
        self,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        add_or_invite_workspace_user(workspace, "hello@example.com")
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": "hello@example.com",
            },
        )
        assert result == {
            "data": {
                "removeUserFromWorkspace": {
                    "uuid": str(workspace.uuid),
                    "userInvitations": [],
                },
            },
        }

    # TODO: Check if this test is in view tests
    @pytest.mark.xfail
    def test_uninvite_on_no_invite(
        self,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": "hello@example.com",
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestDeleteWorkspaceBoardSectionMutation:
    """Test DeleteWorkspaceBoardMutation."""

    query = """
mutation DeleteWorkspaceBoardSection($uuid: UUID!) {
    deleteWorkspaceBoardSection(input: {uuid: $uuid}) {
        uuid
    }
}
"""

    # TODO: Check if this test is in services tests
    @pytest.mark.xfail
    def test_still_has_tasks(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
        task,
    ):
        """Assert section is not deleted if tasks still exist."""
        count = models.WorkspaceBoardSection.objects.count()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert "still has tasks" in str(result)
        assert models.WorkspaceBoardSection.objects.count() == count
