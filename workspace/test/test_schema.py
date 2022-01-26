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


@pytest.mark.django_db
class TestTopLevelResolvers:
    """Test top level resolvers."""

    query = """
query All(
  $workspaceUuid: ID!, $workspaceBoardUuid: ID!,
  $workspaceBoardSectionUuid: ID!, $taskUuid: ID!, $subTaskUuid: ID!) {
  workspace(uuid: $workspaceUuid) {
    title
  }
  workspaceBoard(uuid: $workspaceBoardUuid) {
    title
  }
  workspaceBoardSection(uuid: $workspaceBoardSectionUuid) {
    title
  }
  task(uuid: $taskUuid) {
    title
  }
  subTask(uuid: $subTaskUuid) {
    title
  }
}
"""

    def test_query(
        self,
        workspace,
        workspace_board,
        workspace_board_section,
        task,
        sub_task,
        graphql_query_user,
        workspace_user,
        json_loads,
    ):
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "workspaceUuid": str(workspace.uuid),
                    "workspaceBoardUuid": str(workspace_board.uuid),
                    "workspaceBoardSectionUuid": str(
                        workspace_board_section.uuid,
                    ),
                    "taskUuid": str(task.uuid),
                    "subTaskUuid": str(sub_task.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "workspace": {
                    "title": workspace.title,
                },
                "workspaceBoard": {
                    "title": workspace_board.title,
                },
                "workspaceBoardSection": {
                    "title": workspace_board_section.title,
                },
                "task": {
                    "title": task.title,
                },
                "subTask": {
                    "title": sub_task.title,
                },
            },
        }


@pytest.mark.django_db
class TestMoveTaskMutation:
    """Test MoveTaskMutation."""

    query = """
mutation MoveTask($taskUuid: ID!, $sectionUuid: ID!) {
  moveTask(input: {taskUuid: $taskUuid,
      workspaceBoardSectionUuid: $sectionUuid, position: 2}) {
    task {
      title
    }
  }
}

"""

    def test_move(
        self,
        task,
        other_task,
        workspace_board_section,
        graphql_query_user,
        workspace_user,
        json_loads,
    ):
        """Test moving."""
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "taskUuid": str(task.uuid),
                    "sectionUuid": str(workspace_board_section.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "moveTask": {
                    "task": {
                        "title": task.title,
                    }
                }
            }
        }
