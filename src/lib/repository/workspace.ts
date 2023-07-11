import {
    Mutation_MoveWorkspaceBoardSection,
    Mutation_AddLabelMutation,
    Mutation_AddTask,
    Mutation_AddWorkspaceBoard,
    Mutation_AddWorkspaceBoardSection,
    Mutation_ArchiveWorkspaceBoard,
    Mutation_AssignLabel,
    Mutation_AssignTask,
    Mutation_DeleteLabelMutation,
    Mutation_MoveTaskAfter,
    Mutation_UpdateLabelMutation,
    Mutation_UpdateTask,
    Mutation_DeleteTask,
    Mutation_UpdateWorkspaceBoard,
} from "$lib/graphql/operations";
import type {
    CreateTask,
    CreateWorkspaceBoardSection,
    Label,
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";
import { getWithCredentialsJson } from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";

import { client } from "$lib/graphql/client";

// Task CRUD
// Create
export async function createTask(createTask: CreateTask): Promise<void> {
    await client.mutate({
        mutation: Mutation_AddTask,
        variables: {
            input: {
                title: createTask.title,
                description: createTask.description,
                deadline: createTask.deadline,
                workspaceBoardSectionUuid:
                    createTask.workspace_board_section.uuid,
            },
        },
    });
}

// Update
export async function updateTask(task: Task) {
    await client.mutate({
        mutation: Mutation_UpdateTask,
        variables: {
            input: {
                uuid: task.uuid,
                title: task.title,
                description: task.description,
                deadline: task.deadline ?? null,
                // TODO
                // labels: task.labels.map((l) => l.uuid),
                // TODO
                // assignee: task.assignee ? task.assignee.user.email : null,
            },
        },
    });
}

// XXX
// taskUuid should be first (more invariant than userEmail)
export async function assignUserToTask(
    userEmail: string | null,
    taskUuid: string
): Promise<void> {
    try {
        await client.mutate({
            mutation: Mutation_AssignTask,
            variables: {
                input: {
                    uuid: taskUuid,
                    email: userEmail,
                },
            },
        });
    } catch (error) {
        console.error(error);
    }
}

export async function moveTaskAfter(
    taskUuid: string,
    workspaceBoardSectionUuid: string,
    afterTaskUuid: string | null = null
): Promise<void> {
    try {
        const input: {
            taskUuid: string;
            workspaceBoardSectionUuid: string;
            afterTaskUuid?: string;
        } = {
            taskUuid,
            workspaceBoardSectionUuid,
        };

        if (afterTaskUuid) {
            input.afterTaskUuid = afterTaskUuid;
        }

        await client.mutate({
            mutation: Mutation_MoveTaskAfter,
            variables: { input },
        });
    } catch (error) {
        console.error(error);
    }
}

export async function assignLabelToTask(
    task: Task,
    labelUuid: string,
    assigned: boolean
): Promise<void> {
    const input: {
        taskUuid: string;
        labelUuid: string;
        assigned: boolean;
    } = {
        taskUuid: task.uuid,
        labelUuid,
        assigned,
    };
    await client.mutate({
        mutation: Mutation_AssignLabel,
        variables: {
            input,
        },
    });
}

// Delete
export async function deleteTask(task: Task): Promise<void> {
    await client.mutate({
        mutation: Mutation_DeleteTask,
        variables: {
            input: {
                uuid: task.uuid,
            },
        },
    });
}
// Label CRUD
export async function createLabel(
    workspace: Workspace,
    name: string,
    color: number
) {
    await client.mutate({
        mutation: Mutation_AddLabelMutation,
        variables: {
            input: {
                workspaceUuid: workspace.uuid,
                name,
                color,
            },
        },
    });
}
export async function updateLabel(label: Label, name: string, color: number) {
    await client.mutate({
        mutation: Mutation_UpdateLabelMutation,
        variables: {
            input: {
                uuid: label.uuid,
                name,
                color,
            },
        },
    });
}

export async function deleteLabel(label: Label) {
    await client.mutate({
        mutation: Mutation_DeleteLabelMutation,
        variables: {
            input: {
                uuid: label.uuid,
            },
        },
    });
}

// WorkspaceBoard CRUD
// Create
export async function createWorkspaceBoard(
    workspace: Workspace,
    workspaceBoard: { title: string; description: string; deadline: null }
): Promise<{ uuid: string }> {
    const input = {
        workspaceUuid: workspace.uuid,
        ...workspaceBoard,
    };
    interface result {
        data: { addWorkspaceBoard: WorkspaceBoard };
    }
    const created = (await client.mutate({
        mutation: Mutation_AddWorkspaceBoard,
        variables: {
            input,
        },
    })) as result;
    console.log(created);
    const {
        data: { addWorkspaceBoard },
    } = created;
    return addWorkspaceBoard;
}

// Read
export async function getWorkspaceBoard(
    uuid: string,
    repositoryContext?: RepositoryContext
): Promise<WorkspaceBoard> {
    return await getWithCredentialsJson<WorkspaceBoard>(
        `/workspace/workspace-board/${uuid}`,
        repositoryContext
    );
}

export async function getWorkspaceBoardSection(
    uuid: string,
    repositoryContext?: RepositoryContext
): Promise<WorkspaceBoardSection> {
    return await getWithCredentialsJson<WorkspaceBoardSection>(
        `/workspace/workspace-board-section/${uuid}`,
        repositoryContext
    );
}

export async function getWorkspaces(
    repositoryContext?: RepositoryContext
): Promise<Workspace[]> {
    return await getWithCredentialsJson<Workspace[]>(
        `/workspace/user/workspaces/`,
        repositoryContext
    );
}

export async function getWorkspace(
    uuid: string,
    repositoryContext?: RepositoryContext
): Promise<Workspace> {
    return await getWithCredentialsJson<Workspace>(
        `/workspace/workspace/${uuid}`,
        repositoryContext
    );
}

export async function getTask(
    uuid: string,
    repositoryContext?: RepositoryContext
): Promise<Task> {
    return await getWithCredentialsJson<Task>(
        `/workspace/task/${uuid}`,
        repositoryContext
    );
}

export async function getArchivedWorkspaceBoards(
    workspace_uuid: string
): Promise<WorkspaceBoard[]> {
    return await getWithCredentialsJson<WorkspaceBoard[]>(
        `/workspace/workspace/${workspace_uuid}/workspace-boards-archived/`
    );
}

// These methods find refuge from SelectWorkspaceBoard.svelte here
export async function updateWorkspaceBoard(workspaceBoard: WorkspaceBoard) {
    await client.mutate({
        mutation: Mutation_UpdateWorkspaceBoard,
        variables: {
            input: {
                uuid: workspaceBoard.uuid,
                title: workspaceBoard.title,
                deadline: workspaceBoard.deadline,
                description: "",
            },
        },
    });
}

export async function archiveWorkspaceBoard(workspaceBoard: WorkspaceBoard) {
    // TODO confirmation dialog
    await client.mutate({
        mutation: Mutation_ArchiveWorkspaceBoard,
        variables: {
            input: {
                uuid: workspaceBoard.uuid,
                archived: true,
            },
        },
    });

    // TODO here we ought to find out the URL of the workspace this
    // workspace board belongs to
    console.error("TODO");
}

// WorkspaceBoardSection CRUD
// Create
export async function createWorkspaceBoardSection(
    workspaceBoard: WorkspaceBoard,
    workspaceBoardSection: CreateWorkspaceBoardSection
) {
    await client.mutate({
        mutation: Mutation_AddWorkspaceBoardSection,
        variables: {
            input: {
                workspaceBoardUuid: workspaceBoard.uuid,
                ...workspaceBoardSection,
            },
        },
    });
}

// Read
// Update
export async function moveWorkspaceBoardSection(
    { uuid }: WorkspaceBoardSection,
    order: number
) {
    await client.mutate({
        mutation: Mutation_MoveWorkspaceBoardSection,
        variables: {
            input: {
                workspaceBoardSectionUuid: uuid,
                order,
            },
        },
    });
}
