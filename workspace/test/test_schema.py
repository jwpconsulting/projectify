"""Test workspace schema."""
import pytest


@pytest.mark.django_db
class TestBigQuery:
    """Test a big query."""

    query = """
{
  user {
    email
  }
  workspaces {
    boards {
      sections {
        tasks {
          subTasks {
            title
          }
        }
      }
    }
  }
}

"""

    def test_big_query(
        self,
        graphql_query_user,
        workspace_user,
        user,
        json_loads,
        sub_task,
    ):
        """Assert that the big query works."""
        result = json_loads(graphql_query_user(self.query).content)
        sections = result["data"]["workspaces"][0]["boards"][0]["sections"][0]
        assert sections["tasks"][0]["subTasks"][0]["title"] == sub_task.title
