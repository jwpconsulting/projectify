"""Test workspace queries."""
from django.contrib import (
    auth,
)

import pytest

from ... import (
    factory,
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
    labels {
      uuid
    }
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
        sub_task,
        label,
        chat_message,
    ):
        """Assert that the big query works."""
        result = graphql_query_user(self.query)
        assert "errors" not in result, result
        workspace = result["data"]["workspaces"][0]
        labels = workspace["labels"]
        assert labels[0]["uuid"] == str(label.uuid)
        sections = workspace["boards"][0]["sections"][0]
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
    assignee {
      email
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
    author {
      email
    }
  }
}
"""

    def test_query(
        self,
        user,
        workspace,
        workspace_board,
        workspace_board_section,
        workspace_user,
        task,
        sub_task,
        chat_message,
        graphql_query_user,
    ):
        """Test query."""
        result = graphql_query_user(
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
                    "assignee": {
                        "email": user.email,
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
                    "author": {
                        "email": workspace_user.user.email,
                    },
                },
            },
        }


@pytest.mark.django_db
class TestWorkspace:
    """Test workspace field."""

    def test_redeemed_invite(
        self,
        user,
        workspace,
        workspace_user,
        graphql_query_user,
        workspace_user_invite,
    ):
        """Ensure that invites disappear once redeemed."""
        query = """
query Workspace($uuid: ID!) {
    workspace(uuid: $uuid) {
        users {
            email
        }
        userInvitations {
            email
        }
    }
}
"""
        result = graphql_query_user(
            query,
            variables={
                "uuid": str(workspace.uuid),
            },
        )
        email = workspace_user_invite.user_invite.email
        assert result == {
            "data": {
                "workspace": {
                    "users": [
                        {
                            "email": user.email,
                        },
                    ],
                    "userInvitations": [
                        {
                            "email": email,
                        },
                    ],
                },
            },
        }
        User = auth.get_user_model()
        User.objects.create_user(email)
        result = graphql_query_user(
            query,
            variables={
                "uuid": str(workspace.uuid),
            },
        )
        assert result == {
            "data": {
                "workspace": {
                    "users": [
                        {
                            "email": user.email,
                        },
                        {
                            "email": email,
                        },
                    ],
                    "userInvitations": [],
                },
            },
        }


@pytest.mark.django_db
class TestWorkspaces:
    """Test workspaces field."""

    def test_boards(
        self,
        user,
        workspace_board,
        workspace_user,
        graphql_query_user,
    ):
        """Test retrieving non-archived boards."""
        query = """
query {
    workspaces {
        boards {
            uuid
        }
    }
}
"""
        result = graphql_query_user(
            query,
        )
        assert result == {
            "data": {
                "workspaces": [
                    {
                        "boards": [
                            {
                                "uuid": str(workspace_board.uuid),
                            },
                        ],
                    },
                ]
            },
        }

    def test_archived_boards(
        self,
        user,
        workspace,
        workspace_board,
        workspace_user,
        graphql_query_user,
    ):
        """Test retrieving archived boards."""
        query = """
query {
    workspaces {
        archivedBoards {
            uuid
        }
    }
}
"""
        other_workspace_board = factory.WorkspaceBoardFactory(
            workspace=workspace,
        )
        other_workspace_board.archive()
        result = graphql_query_user(
            query,
        )
        assert result == {
            "data": {
                "workspaces": [
                    {
                        "archivedBoards": [
                            {
                                "uuid": str(other_workspace_board.uuid),
                            },
                        ],
                    },
                ]
            },
        }
