"""Test workspace mutations."""
from django.utils import (
    timezone,
)

import pytest

from workspace.models.workspace_user_invite import (
    add_or_invite_workspace_user,
)
from workspace.services.workspace import workspace_add_user

from ... import (
    models,
)


@pytest.mark.django_db
class TestMoveWorkspaceBoardSectionMutation:
    """Test MoveWorkspaceBoardSectionMutation."""

    query = """
mutation MoveWorkspaceBoardSection($uuid: UUID!) {
    moveWorkspaceBoardSection(
        input:{workspaceBoardSectionUuid: $uuid, order: 1 }
    ) {
        uuid
        order
    }
}
"""

    def test_query(
        self,
        workspace_board_section,
        other_workspace_board_section,
        graphql_query_user,
        workspace_user,
    ):
        """Test the query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "moveWorkspaceBoardSection": {
                    "uuid": str(workspace_board_section.uuid),
                    "order": 1,
                },
            },
        }


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

    def test_query_unauthorized(
        self,
        other_user,
        graphql_query_user,
        workspace,
    ):
        """Test query."""
        workspace_add_user(workspace, other_user)
        assert workspace.users.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": other_user.email,
            },
        )
        assert "errors" in result
        assert workspace.users.count() == 1

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


# Add Mutations
@pytest.mark.django_db
class TestAddWorkspaceBoardMutation:
    """Test AddWorkspaceBoard."""

    query = """
mutation AddWorkspaceBoard(
    $workspaceUuid: UUID!,
    $title: String!,
    $description: String!,
    $deadline: DateTime
) {
    addWorkspaceBoard(input: {
        workspaceUuid: $workspaceUuid,
        title: $title,
        description: $description,
        deadline: $deadline
    }) {
        title
        description
        deadline
    }
}
"""

    query_no_deadline = """
mutation AddWorkspaceBoard($workspaceUuid: UUID!) {
    addWorkspaceBoard(input: {
        workspaceUuid: $workspaceUuid,
        title: "Hello",
        description: "World"
    }) {
        title
        description
        deadline
    }
}
"""

    def test_query(
        self,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        now = timezone.now().isoformat()
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceUuid": str(workspace.uuid),
                "title": "Hello",
                "description": "World",
                "deadline": now,
            },
        )
        assert result == {
            "data": {
                "addWorkspaceBoard": {
                    "title": "Hello",
                    "description": "World",
                    "deadline": now,
                }
            }
        }

    def test_query_no_deadline(
        self,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query with no deadline specified."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceUuid": str(workspace.uuid),
                "title": "Hello",
                "description": "World",
                "deadline": None,
            },
        )
        assert result == {
            "data": {
                "addWorkspaceBoard": {
                    "title": "Hello",
                    "description": "World",
                    "deadline": None,
                }
            }
        }

    def test_query_no_deadline_unset(
        self,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query with no deadline specified."""
        result = graphql_query_user(
            self.query_no_deadline,
            variables={
                "workspaceUuid": str(workspace.uuid),
            },
        )
        assert result == {
            "data": {
                "addWorkspaceBoard": {
                    "title": "Hello",
                    "description": "World",
                    "deadline": None,
                }
            }
        }


@pytest.mark.django_db
class TestAddLabelMutation:
    """Test AddLabelMutation."""

    query = """
mutation AddLabel($workspaceUuid: UUID!) {
    addLabel(input: {
        workspaceUuid: $workspaceUuid,
        color: 1, name: "important"
    }) {
        name
        color
        workspace {
            uuid
        }
    }
}
"""

    def test_query(self, workspace, workspace_user, graphql_query_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceUuid": str(workspace.uuid),
            },
        )
        assert result == {
            "data": {
                "addLabel": {
                    "name": "important",
                    "color": 1,
                    "workspace": {
                        "uuid": str(workspace.uuid),
                    },
                },
            }
        }


@pytest.mark.django_db
class TestAddChatMessageMutation:
    """Test AddChatMessageMutation."""

    query = """
mutation AddChatMessage($uuid: UUID!) {
    addChatMessage(input:{taskUuid: $uuid, text:"Hello world"}) {
        text
    }
}
"""

    def test_query(self, graphql_query_user, task, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert result == {
            "data": {
                "addChatMessage": {
                    "text": "Hello world",
                },
            },
        }

    def test_query_unauthorized(
        self, graphql_query_user, task, workspace_user
    ):
        """Test query."""
        workspace_user.delete()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestAssignLabelMutation:
    """Test AssignLabelMutation."""

    query = """
mutation AssignLabel(
    $taskUuid: UUID!, $labelUuid: UUID!, $assigned: Boolean!
) {
    assignLabel(input: {
        taskUuid: $taskUuid, labelUuid: $labelUuid, assigned: $assigned
    }) {
        uuid
        labels {
            uuid
        }
    }
}
"""

    def test_query_assign(
        self,
        graphql_query_user,
        task,
        label,
        workspace_user,
    ):
        """Test assigning."""
        result = graphql_query_user(
            self.query,
            variables={
                "taskUuid": str(task.uuid),
                "labelUuid": str(label.uuid),
                "assigned": True,
            },
        )
        assert result == {
            "data": {
                "assignLabel": {
                    "uuid": str(task.uuid),
                    "labels": [
                        {
                            "uuid": str(label.uuid),
                        },
                    ],
                }
            }
        }

    def test_query_unassign(
        self,
        graphql_query_user,
        task,
        label,
        workspace_user,
    ):
        """Test unassigning."""
        task.add_label(label)
        result = graphql_query_user(
            self.query,
            variables={
                "taskUuid": str(task.uuid),
                "labelUuid": str(label.uuid),
                "assigned": False,
            },
        )
        assert result == {
            "data": {
                "assignLabel": {
                    "uuid": str(task.uuid),
                    "labels": [],
                }
            }
        }


# Update Mutations
@pytest.mark.django_db
class TestUpdateWorkspaceMutation:
    """Test UpdateWorkspaceMutation."""

    query = """
mutation UpdateWorkspace($uuid: UUID!) {
    updateWorkspace(input: {uuid: $uuid, title: "foo", description: "bar"}) {
        uuid
        title
        description
    }
}

"""

    def test_query(
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
            },
        )
        assert result == {
            "data": {
                "updateWorkspace": {
                    "uuid": str(workspace.uuid),
                    "title": "foo",
                    "description": "bar",
                },
            },
        }

    def test_query_unauthorized(
        self,
        graphql_query_user,
        workspace,
    ):
        """Test with unauthorized user."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestUpdateWorkspaceUserMutation:
    """Test UpdateWorkspaceUserMutation."""

    query = """
mutation UpdateWorkspaceUser(
    $workspaceUuid: UUID!,
    $email: String!,
    $role: WorkspaceUserRole!
) {
    updateWorkspaceUser(
        input: {
            workspaceUuid: $workspaceUuid,
            email: $email,
            jobTitle: "Expert Knob Twiddler",
            role: $role,
        }
    ) {
        email
        role
        jobTitle
    }
}

"""

    def test_query(
        self,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceUuid": str(workspace.uuid),
                "email": workspace_user.user.email,
                "role": "OBSERVER",
            },
        )
        assert result == {
            "data": {
                "updateWorkspaceUser": {
                    "email": workspace_user.user.email,
                    "jobTitle": "Expert Knob Twiddler",
                    "role": "OBSERVER",
                },
            },
        }


@pytest.mark.django_db
class TestArchiveWorkspaceBoardMutation:
    """Test ArchiveWorkspaceBoardMutation."""

    query = """
mutation ArchiveWorkspaceBoard($uuid: UUID!, $archived: Boolean!) {
    archiveWorkspaceBoard(input: {uuid: $uuid, archived: $archived}) {
        uuid
        archived
    }
}
"""

    def test_archive(
        self,
        graphql_query_user,
        workspace_board,
        workspace_user,
    ):
        """Test archiving."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
                "archived": True,
            },
        )
        workspace_board.refresh_from_db()
        assert result == {
            "data": {
                "archiveWorkspaceBoard": {
                    "uuid": str(workspace_board.uuid),
                    "archived": workspace_board.archived.isoformat(),
                },
            },
        }

    def test_unarchive(
        self,
        graphql_query_user,
        workspace_board,
        workspace_user,
    ):
        """Test unarchiving."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
                "archived": False,
            },
        )
        assert result == {
            "data": {
                "archiveWorkspaceBoard": {
                    "uuid": str(workspace_board.uuid),
                    "archived": None,
                },
            },
        }


@pytest.mark.django_db
class TestUpdateWorkspaceBoardMutation:
    """Test UpdateWorkspaceBoardMutation."""

    query = """
mutation UpdateWorkspaceBoard($uuid: UUID!, $deadline: DateTime) {
    updateWorkspaceBoard(input: {
        uuid: $uuid,
        title: "Foo",
        description: "Bar",
        deadline: $deadline
    }) {
        title
        description
        deadline
    }
}
"""

    def test_query(self, graphql_query_user, workspace_board, workspace_user):
        """Test query."""
        assert workspace_board.deadline
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
                "deadline": None,
            },
        )
        assert result == {
            "data": {
                "updateWorkspaceBoard": {
                    "title": "Foo",
                    "description": "Bar",
                    "deadline": None,
                },
            },
        }
        workspace_board.refresh_from_db()
        assert workspace_board.deadline is None

    def test_set_deadline(
        self,
        graphql_query_user,
        workspace_board,
        workspace_user,
    ):
        """Test query."""
        now = timezone.now().isoformat()
        result = graphql_query_user(
            self.query,
            variables={
                "deadline": now,
                "uuid": str(workspace_board.uuid),
            },
        )
        assert result == {
            "data": {
                "updateWorkspaceBoard": {
                    "title": "Foo",
                    "description": "Bar",
                    "deadline": now,
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, workspace_board):
        """Test query when user not authorized."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
                "deadline": None,
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestUpdateWorkspaceBoardSectionMutation:
    """Test UpdateWorkspaceBoardSectionMutation."""

    query = """
mutation UpdateWorkspaceBoardSection($uuid: UUID!) {
    updateWorkspaceBoardSection(input: {
        uuid: $uuid, title: "Foo", description: "Bar"}
    ) {
        title
        description
    }
}
"""

    def test_query(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "updateWorkspaceBoardSection": {
                    "title": "Foo",
                    "description": "Bar",
                },
            },
        }

    def test_query_unauthorized(
        self,
        graphql_query_user,
        workspace_board_section,
    ):
        """Test query when user not authorized."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestUpdateLabelMutation:
    """Test UpdateLabelMutation."""

    query = """
mutation UpdateLabel($uuid: UUID!) {
    updateLabel(input: {uuid: $uuid, name: "Friendship", color: 199}) {
        name
        color
    }
}
"""

    def test_query(self, graphql_query_user, label, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(label.uuid),
            },
        )
        assert result == {
            "data": {
                "updateLabel": {
                    "name": "Friendship",
                    "color": 199,
                },
            },
        }


# Delete Mutations
@pytest.mark.django_db
class TestDeleteWorkspaceBoardMutation:
    """Test DeleteWorkspaceBoardMutation."""

    query = """
mutation DeleteWorkspaceBoard($uuid: UUID!) {
    deleteWorkspaceBoard(input: {uuid: $uuid}) {
        uuid
    }
}
"""

    def test_query(
        self,
        graphql_query_user,
        workspace_board,
        workspace_user,
    ):
        """Test query."""
        count = models.WorkspaceBoard.objects.count()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteWorkspaceBoard": {
                    "uuid": str(workspace_board.uuid),
                }
            }
        }
        assert models.WorkspaceBoard.objects.count() == count - 1

    def test_query_unauthorized(self, graphql_query_user, workspace_board):
        """Test query."""
        count = models.WorkspaceBoard.objects.count()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
            },
        )
        assert "errors" in result
        assert models.WorkspaceBoard.objects.count() == count


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

    def test_query(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
    ):
        """Test query."""
        count = models.WorkspaceBoardSection.objects.count()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteWorkspaceBoardSection": {
                    "uuid": str(workspace_board_section.uuid),
                }
            }
        }
        assert models.WorkspaceBoardSection.objects.count() == count - 1

    def test_query_unauthorized(
        self,
        graphql_query_user,
        workspace_board_section,
    ):
        """Test query."""
        count = models.WorkspaceBoardSection.objects.count()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert models.WorkspaceBoardSection.objects.count() == count
        assert "errors" in result

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


@pytest.mark.django_db
class TestDeleteTask:
    """Test DeleteTask."""

    query = """
mutation DeleteTask($uuid: UUID!) {
    deleteTask(input: {uuid: $uuid}) {
        uuid
    }
}
"""

    def test_query(
        self,
        graphql_query_user,
        task,
        workspace_user,
        chat_message,
        sub_task,
    ):
        """Test query."""
        count = models.Task.objects.count()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteTask": {
                    "uuid": str(task.uuid),
                }
            }
        }
        assert models.Task.objects.count() == count - 1

    def test_query_unauthorized(
        self, graphql_query_user, task, workspace_user
    ):
        """Test query."""
        workspace_user.delete()
        count = models.Task.objects.count()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert models.Task.objects.count() == count
        assert "errors" in result


@pytest.mark.django_db
class TestDeleteLabel:
    """Test DeleteLabelMutation."""

    query = """
mutation DeleteLabel($uuid: UUID!) {
    deleteLabel(input: {uuid: $uuid}) {
        uuid
    }
}
"""

    def test_query(self, graphql_query_user, label, workspace_user):
        """Test query."""
        count = models.Label.objects.count()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(label.uuid),
            },
        )
        assert result == {
            "data": {
                "deleteLabel": {
                    "uuid": str(label.uuid),
                },
            },
        }
        assert models.Label.objects.count() == count - 1
