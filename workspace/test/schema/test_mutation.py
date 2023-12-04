"""Test workspace mutations."""
import pytest

from ... import (
    models,
)


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
