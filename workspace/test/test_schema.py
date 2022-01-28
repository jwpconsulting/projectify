"""Test workspace schema."""
import pytest

from .. import (
    factory,
    models,
)


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
          chatMessages {
            text
          }
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
        chat_message,
    ):
        """Assert that the big query works."""
        result = json_loads(graphql_query_user(self.query).content)
        assert "errors" not in result, result
        sections = result["data"]["workspaces"][0]["boards"][0]["sections"][0]
        tasks = sections["tasks"]
        sub_tasks = tasks[0]["subTasks"]
        assert sub_tasks[0]["title"] == sub_task.title
        assert tasks[0]["chatMessages"][0]["text"] == chat_message.text


@pytest.mark.django_db
class TestTopLevelResolvers:
    """Test top level resolvers."""

    query = """
query All(
  $workspaceUuid: ID!, $workspaceBoardUuid: ID!,
  $workspaceBoardSectionUuid: ID!, $taskUuid: ID!, $subTaskUuid: ID!,
  $chatMessageUuid: ID!
) {
  workspace(uuid: $workspaceUuid) {
    title
  }
  workspaceBoard(uuid: $workspaceBoardUuid) {
    title
    workspace {
      title
    }
  }
  workspaceBoardSection(uuid: $workspaceBoardSectionUuid) {
    title
    workspaceBoard {
      title
    }
  }
  task(uuid: $taskUuid) {
    title
    workspaceBoardSection {
      title
    }
  }
  subTask(uuid: $subTaskUuid) {
    title
    task {
      title
    }
  }
  chatMessage(uuid: $chatMessageUuid) {
    text
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
        chat_message,
        graphql_query_user,
        workspace_user,
        json_loads,
    ):
        """Test query."""
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
                    "chatMessageUuid": str(chat_message.uuid),
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
                    "workspace": {
                        "title": workspace.title,
                    },
                },
                "workspaceBoardSection": {
                    "title": workspace_board_section.title,
                    "workspaceBoard": {
                        "title": workspace_board.title,
                    },
                },
                "task": {
                    "title": task.title,
                    "workspaceBoardSection": {
                        "title": workspace_board_section.title,
                    },
                },
                "subTask": {
                    "title": sub_task.title,
                    "task": {
                        "title": task.title,
                    },
                },
                "chatMessage": {
                    "text": chat_message.text,
                },
            },
        }


@pytest.mark.django_db
class TestChangeSubTaskDoneMutation:
    """Test ChangeSubTaskDoneMutation."""

    query = """
mutation ChangeSubTaskDone($uuid: ID!) {
  changeSubTaskDone(input: {subTaskUuid: $uuid, done: true}) {
    subTask {
      done
    }
  }
}
"""

    def test_query(
        self,
        graphql_query_user,
        json_loads,
        workspace_user,
        sub_task,
    ):
        """Test query."""
        assert sub_task.done is False
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "uuid": str(sub_task.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "changeSubTaskDone": {
                    "subTask": {
                        "done": True,
                    },
                },
            },
        }


@pytest.mark.django_db
class TestMoveWorkspaceBoardSectionMutation:
    """Test MoveWorkspaceBoardSectionMutation."""

    query = """
mutation MoveWorkspaceBoardSection($uuid: ID!) {
  moveWorkspaceBoardSection(
    input:{workspaceBoardSectionUuid: $uuid, order: 1 }
  ) {
    workspaceBoardSection {
      uuid
      order
    }
  }
}
"""

    def test_query(
        self,
        workspace_board_section,
        graphql_query_user,
        workspace_user,
        json_loads,
    ):
        """Test the query."""
        factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board_section.workspace_board,
        )
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "uuid": str(workspace_board_section.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "moveWorkspaceBoardSection": {
                    "workspaceBoardSection": {
                        "uuid": str(workspace_board_section.uuid),
                        "order": 1,
                    },
                },
            },
        }


@pytest.mark.django_db
class TestMoveTaskMutation:
    """Test MoveTaskMutation."""

    query = """
mutation MoveTask($taskUuid: ID!, $sectionUuid: ID!) {
  moveTask(input: {taskUuid: $taskUuid,
      workspaceBoardSectionUuid: $sectionUuid, order: 2}) {
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


# Add Mutations
@pytest.mark.django_db
class TestAddChatMessageMutation:
    """Test AddChatMessageMutation."""

    query = """
mutation AddChatMessage($uuid: ID!) {
  addChatMessage(input:{taskUuid: $uuid, text:"Hello world"}) {
    chatMessage {
      text
    }
  }
}
"""

    def test_query(self, graphql_query_user, json_loads, task, workspace_user):
        """Test query."""
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "uuid": str(task.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "addChatMessage": {
                    "chatMessage": {
                        "text": "Hello world",
                    },
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, json_loads, task):
        """Test query."""
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "uuid": str(task.uuid),
                },
            ).content,
        )
        assert "errors" in result


# Update Mutations
@pytest.mark.django_db
class TestUpdateWorkspaceMutation:
    """Test UpdateWorkspaceMutation."""

    query = """
mutation UpdateWorkspace($uuid: ID!) {
  updateWorkspace(input: {uuid: $uuid, title: "foo", description: "bar"}) {
    workspace {
      uuid
      title
      description
    }
  }
}

"""

    def test_query(
        self,
        graphql_query_user,
        json_loads,
        workspace,
        workspace_user,
    ):
        """Test query."""
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "uuid": str(workspace.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "updateWorkspace": {
                    "workspace": {
                        "uuid": str(workspace.uuid),
                        "title": "foo",
                        "description": "bar",
                    },
                },
            },
        }

    def test_query_unauthorized(
        self,
        graphql_query_user,
        json_loads,
        workspace,
    ):
        """Test with unauthorized user."""
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "uuid": str(workspace.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "updateWorkspace": None,
            },
            "errors": [
                {
                    "locations": [{"column": 3, "line": 3}],
                    "message": "Workspace matching query does not exist.",
                    "path": ["updateWorkspace"],
                },
            ],
        }


# Delete Mutations
@pytest.mark.django_db
class TestDeleteWorkspaceBoardMutation:
    """Test DeleteWorkspaceBoardMutation."""

    query = """
mutation DeleteWorkspaceBoard($uuid: ID!) {
  deleteWorkspaceBoard(uuid: $uuid) {
    workspaceBoard {
      uuid
    }
  }
}
"""

    def test_query(
        self,
        graphql_query_user,
        json_loads,
        workspace_board,
        workspace_user,
    ):
        """Test query."""
        assert models.WorkspaceBoard.objects.count() == 1
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "uuid": str(workspace_board.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "deleteWorkspaceBoard": {
                    "workspaceBoard": {
                        "uuid": str(workspace_board.uuid),
                    }
                }
            }
        }
        assert models.WorkspaceBoard.objects.count() == 0

    def test_query_unauthorized(
        self,
        graphql_query_user,
        json_loads,
        workspace_board,
    ):
        """Test query."""
        assert models.WorkspaceBoard.objects.count() == 1
        result = json_loads(
            graphql_query_user(
                self.query,
                variables={
                    "uuid": str(workspace_board.uuid),
                },
            ).content,
        )
        assert result == {
            "data": {
                "deleteWorkspaceBoard": None,
            },
            "errors": [
                {
                    "locations": [{"column": 3, "line": 3}],
                    "message": "WorkspaceBoard matching query does not exist.",
                    "path": ["deleteWorkspaceBoard"],
                },
            ],
        }
        assert models.WorkspaceBoard.objects.count() == 1
