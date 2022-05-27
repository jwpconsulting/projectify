"""Test workspace mutations."""
from datetime import (
    datetime,
)

from django.utils import (
    timezone,
)

import pytest

from ... import (
    factory,
    models,
)


@pytest.mark.django_db
class TestChangeSubTaskDoneMutation:
    """Test ChangeSubTaskDoneMutation."""

    query = """
mutation ChangeSubTaskDone($uuid: UUID!) {
    changeSubTaskDone(input: {subTaskUuid: $uuid, done: true}) {
        done
    }
}
"""

    def test_query(
        self,
        graphql_query_user,
        workspace_user,
        sub_task,
    ):
        """Test query."""
        assert sub_task.done is False
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert result == {
            "data": {
                "changeSubTaskDone": {
                    "done": True,
                },
            },
        }


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
        graphql_query_user,
        workspace_user,
    ):
        """Test the query."""
        factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board_section.workspace_board,
        )
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
class TestMoveTaskMutation:
    """Test MoveTaskMutation."""

    query = """
mutation MoveTask($taskUuid: UUID!, $sectionUuid: UUID!) {
    moveTask(input: {taskUuid: $taskUuid,
        workspaceBoardSectionUuid: $sectionUuid, order: 2}
    ) {
        title
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
    ):
        """Test moving."""
        result = graphql_query_user(
            self.query,
            variables={
                "taskUuid": str(task.uuid),
                "sectionUuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "moveTask": {
                    "title": task.title,
                }
            }
        }


@pytest.mark.django_db
class TestMoveTaskAfterMutation:
    """Test MoveTaskAfterMutation."""

    query = """
mutation MoveTaskAfter(
    $taskUuid: UUID!,
    $afterTaskUuid: UUID!,
    $sectionUuid: UUID!
) {
    moveTaskAfter(
        input: {
            taskUuid: $taskUuid,
            afterTaskUuid: $afterTaskUuid,
            workspaceBoardSectionUuid: $sectionUuid
        }
    ) {
        title
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
    ):
        """Test moving."""
        tasks = list(models.Task.objects.all().values("uuid"))
        assert tasks == [
            {"uuid": task.uuid},
            {"uuid": other_task.uuid},
        ]
        result = graphql_query_user(
            self.query,
            variables={
                "taskUuid": str(task.uuid),
                "afterTaskUuid": str(other_task.uuid),
                "sectionUuid": str(workspace_board_section.uuid),
            },
        )
        assert result == {
            "data": {
                "moveTaskAfter": {
                    "title": task.title,
                }
            }
        }
        tasks = list(models.Task.objects.all().values("uuid"))
        assert tasks == [
            {"uuid": other_task.uuid},
            {"uuid": task.uuid},
        ]


@pytest.mark.django_db
class TestMoveSubTaskMutation:
    """Test MoveSubTaskMutation."""

    query = """
mutation MoveSubTaskMutation($uuid: UUID!) {
    moveSubTask(
        input: {
            subTaskUuid: $uuid,
            order: 1
        }
    ) {
        uuid
        order
    }
}
"""

    def test_query(
        self,
        task,
        sub_task,
        graphql_query_user,
        workspace_user,
    ):
        """Test the query."""
        other_sub_task = factory.SubTaskFactory(
            task=sub_task.task,
        )
        assert list(task.subtask_set.all().values("uuid", "_order")) == [
            {"uuid": sub_task.uuid, "_order": 0},
            {"uuid": other_sub_task.uuid, "_order": 1},
        ]
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert list(task.subtask_set.all().values("uuid", "_order")) == [
            {"uuid": other_sub_task.uuid, "_order": 0},
            {"uuid": sub_task.uuid, "_order": 1},
        ]
        assert result == {
            "data": {
                "moveSubTask": {
                    "uuid": str(sub_task.uuid),
                    "order": 1,
                },
            },
        }


@pytest.mark.django_db
class TestAddUserToWorkspaceMutation:
    """Test AddUserToWorkspaceMutation."""

    query = """
mutation AddUserToWorkspace($uuid: UUID!, $email: String!) {
    addUserToWorkspace(input: {uuid: $uuid, email: $email}) {
        uuid
        userInvitations {
            email
        }
    }
}
"""

    def test_query(
        self,
        task,
        other_user,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": other_user.email,
            },
        )
        assert result == {
            "data": {
                "addUserToWorkspace": {
                    "uuid": str(workspace.uuid),
                    "userInvitations": [],
                },
            },
        }

    def test_query_unauthorized(
        self,
        task,
        other_user,
        graphql_query_user,
        workspace,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": other_user.email,
            },
        )
        assert "errors" in result

    def test_no_user(
        self,
        task,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        assert workspace.users.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace.uuid),
                "email": "hello@example.com",
            },
        )
        assert result == {
            "data": {
                "addUserToWorkspace": {
                    "uuid": str(workspace.uuid),
                    "userInvitations": [
                        {
                            "email": "hello@example.com",
                        },
                    ],
                },
            },
        }
        assert workspace.users.count() == 1
        assert workspace.workspaceuserinvite_set.count() == 1


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
        task,
        other_user,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        workspace.add_user(other_user)
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
        task,
        other_user,
        graphql_query_user,
        workspace,
    ):
        """Test query."""
        workspace.add_user(other_user)
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
        task,
        graphql_query_user,
        workspace,
        workspace_user,
    ):
        """Test query."""
        workspace.invite_user("hello@example.com")
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
        task,
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
class TestAssignTaskMutation:
    """Test AssignTaskMutation."""

    query = """
mutation AssignTask($uuid: UUID!, $email: String) {
    assignTask(input: {uuid: $uuid, email: $email}) {
        assignee {
            email
        }
    }
}
"""

    def test_query(
        self,
        task,
        other_user,
        other_workspace_user,
        graphql_query_user,
        workspace_user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "email": other_user.email,
            },
        )
        assert result == {
            "data": {
                "assignTask": {
                    "assignee": {
                        "email": other_user.email,
                    },
                },
            },
        }

    def test_unassign(
        self,
        task,
        other_user,
        other_workspace_user,
        graphql_query_user,
        workspace_user,
    ):
        """Test query."""
        task.assign_to(other_user)
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "email": None,
            },
        )
        assert result == {
            "data": {
                "assignTask": {
                    "assignee": None,
                },
            },
        }


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


@pytest.mark.django_db
class TestAddTaskMutation:
    """Test AddTask."""

    query = """
mutation AddTask(
    $workspaceBoardSectionUuid: UUID!,
    $deadline: DateTime,
    $assignee: String,
    $subTasks: [String!],
    $labels: [UUID!],
    ) {
    addTask(input: {
        workspaceBoardSectionUuid: $workspaceBoardSectionUuid,
        title: "Hello",
        description: "World",
        deadline: $deadline,
        assignee: $assignee,
        subTasks: $subTasks,
        labels: $labels
    }) {
        title
        description
        deadline
        assignee {
            email
        }
        subTasks {
            title
        }
        labels {
            uuid
        }
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
                "workspaceBoardSectionUuid": str(workspace_board_section.uuid),
                "deadline": None,
            },
        )
        assert result == {
            "data": {
                "addTask": {
                    "title": "Hello",
                    "description": "World",
                    "deadline": None,
                    "assignee": None,
                    "subTasks": [],
                    "labels": [],
                },
            },
        }

    def test_query_deadline(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
    ):
        """Test query."""
        now = timezone.now().isoformat()
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceBoardSectionUuid": str(workspace_board_section.uuid),
                "deadline": now,
            },
        )
        assert result == {
            "data": {
                "addTask": {
                    "title": "Hello",
                    "description": "World",
                    "deadline": now,
                    "assignee": None,
                    "subTasks": [],
                    "labels": [],
                },
            },
        }

    def test_query_assignee(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
        user,
    ):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceBoardSectionUuid": str(workspace_board_section.uuid),
                "deadline": None,
                "assignee": user.email,
            },
        )
        assert result == {
            "data": {
                "addTask": {
                    "title": "Hello",
                    "description": "World",
                    "deadline": None,
                    "assignee": {
                        "email": user.email,
                    },
                    "subTasks": [],
                    "labels": [],
                },
            },
        }

    def test_adding_subtasks(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
        user,
    ):
        """Add subtasks as well."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceBoardSectionUuid": str(workspace_board_section.uuid),
                "deadline": None,
                "subTasks": ["Hello", "World"],
            },
        )
        assert result == {
            "data": {
                "addTask": {
                    "title": "Hello",
                    "description": "World",
                    "deadline": None,
                    "assignee": None,
                    "subTasks": [
                        {
                            "title": "Hello",
                        },
                        {
                            "title": "World",
                        },
                    ],
                    "labels": [],
                },
            },
        }

    def test_assigning_label(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
        user,
        label,
    ):
        """Test assigning a label."""
        result = graphql_query_user(
            self.query,
            variables={
                "workspaceBoardSectionUuid": str(workspace_board_section.uuid),
                "deadline": None,
                "labels": [str(label.uuid)],
            },
        )
        assert result == {
            "data": {
                "addTask": {
                    "title": "Hello",
                    "description": "World",
                    "deadline": None,
                    "assignee": None,
                    "subTasks": [],
                    "labels": [
                        {
                            "uuid": str(label.uuid),
                        },
                    ],
                },
            },
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
class TestAddSubTaskMutation:
    """Test AddSubTaskMutation."""

    query = """
mutation AddSubTask($uuid: UUID!) {
    addSubTask(
        input:{taskUuid: $uuid, title: "Hello world", description: "Foo bar"}
    ) {
        title
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
                "addSubTask": {
                    "title": "Hello world",
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, task):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert "errors" in result


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

    def test_query_unauthorized(self, graphql_query_user, task):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        assert "errors" in result


@pytest.mark.django_db
class TestDuplicateTaskMutation:
    """Test DuplicateTaskMutation."""

    query = """
mutation DuplicateTask($uuid: UUID!) {
    duplicateTask(input: {uuid: $uuid}) {
        uuid
    }
}
"""

    def test_query(self, graphql_query_user, workspace_user, task):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
        new_task = models.Task.objects.last()
        assert result == {
            "data": {
                "duplicateTask": {
                    "uuid": str(new_task.uuid),
                },
            },
        }


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
class TestUpdateTaskMutation:
    """Test TestUpdateTaskMutation."""

    query = """
mutation UpdateTaskMutation($uuid: UUID!, $deadline: DateTime) {
    updateTask(
        input: {
            uuid: $uuid, title: "Foo", description: "Bar", deadline: $deadline
        }
    )
    {
        title
        description
    }
}
"""

    def test_query(self, graphql_query_user, task, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "deadline": None,
            },
        )
        assert result == {
            "data": {
                "updateTask": {
                    "title": "Foo",
                    "description": "Bar",
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, task):
        """Test query when user not authorized."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "deadline": None,
            },
        )
        assert "errors" in result

    def test_assigning_deadline(
        self,
        graphql_query_user,
        task,
        workspace_user,
    ):
        """Test assigning a deadline."""
        deadline = timezone.now()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "deadline": deadline.isoformat(),
            },
        )
        assert "errors" not in result, result
        task.refresh_from_db()
        assert task.deadline == deadline

    def test_assigning_deadline_missing_tz(
        self,
        graphql_query_user,
        task,
        workspace_user,
    ):
        """Test assigning a deadline."""
        deadline = datetime.now()
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "deadline": deadline.isoformat(),
            },
        )
        assert "errors" in result, result

    def test_removing_deadline(
        self,
        graphql_query_user,
        task,
        workspace_user,
    ):
        """Test assigning a deadline."""
        assert task.deadline
        graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
                "deadline": None,
            },
        )
        task.refresh_from_db()
        assert task.deadline is None


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


@pytest.mark.django_db
class TestUpdateSubTaskMutation:
    """Test TestUpdateSubTaskMutation."""

    query = """
mutation UpdateSubTaskMutation($uuid: UUID!) {
    updateSubTask(input: {uuid: $uuid, title: "Foo", description: "Bar"})
    {
        title
        description
    }
}
"""

    def test_query(self, graphql_query_user, sub_task, workspace_user):
        """Test query."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert result == {
            "data": {
                "updateSubTask": {
                    "title": "Foo",
                    "description": "Bar",
                },
            },
        }

    def test_query_unauthorized(self, graphql_query_user, sub_task):
        """Test query when user not authorized."""
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert "errors" in result


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
        assert models.WorkspaceBoard.objects.count() == 1
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
        assert models.WorkspaceBoard.objects.count() == 0

    def test_query_unauthorized(self, graphql_query_user, workspace_board):
        """Test query."""
        assert models.WorkspaceBoard.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board.uuid),
            },
        )
        assert "errors" in result
        assert models.WorkspaceBoard.objects.count() == 1


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
        assert models.WorkspaceBoardSection.objects.count() == 1
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
        assert models.WorkspaceBoardSection.objects.count() == 0

    def test_query_unauthorized(
        self,
        graphql_query_user,
        workspace_board_section,
    ):
        """Test query."""
        assert models.WorkspaceBoardSection.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert "errors" in result

    def test_still_has_tasks(
        self,
        graphql_query_user,
        workspace_board_section,
        workspace_user,
        task,
    ):
        """Assert section is not deleted if tasks still exist."""
        assert models.WorkspaceBoardSection.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(workspace_board_section.uuid),
            },
        )
        assert "still has tasks" in str(result)
        assert models.WorkspaceBoardSection.objects.count() == 1


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
        assert models.Task.objects.count() == 1
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
        assert models.Task.objects.count() == 0

    def test_query_unauthorized(self, graphql_query_user, task):
        """Test query."""
        assert models.Task.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(task.uuid),
            },
        )
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
        assert models.Label.objects.count() == 1
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
        assert models.Label.objects.count() == 0


@pytest.mark.django_db
class TestDeleteSubTask:
    """Test DeleteSubTask."""

    query = """
mutation DeleteSubTask($uuid: UUID!) {
    deleteSubTask(input: {uuid: $uuid}) {
        uuid
    }
}
"""

    def test_query(self, graphql_query_user, sub_task, workspace_user):
        """Test query."""
        assert models.SubTask.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )

        assert result == {
            "data": {
                "deleteSubTask": {
                    "uuid": str(sub_task.uuid),
                }
            }
        }
        assert models.SubTask.objects.count() == 0

    def test_query_unauthorized(self, graphql_query_user, task, sub_task):
        """Test query."""
        assert models.SubTask.objects.count() == 1
        result = graphql_query_user(
            self.query,
            variables={
                "uuid": str(sub_task.uuid),
            },
        )
        assert "errors" in result
