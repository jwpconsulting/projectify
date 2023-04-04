import {
    Mutation_MoveTaskAfter,
    Mutation_AssignTask,
    Mutation_AddLabelMutation,
    Mutation_UpdateLabelMutation,
    Mutation_DeleteLabelMutation,
} from "$lib/graphql/operations";
import type {
    Label,
    WorkspaceBoard,
    Workspace,
    Task,
} from "$lib/types/workspace";
import { getWithCredentialsJson } from "$lib/repository/util";

import { client } from "$lib/graphql/client";

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

export async function deleteTask(task: Task): Promise<void> {
    console.error("TODO do something with", task);
    // TODO const modalRes = await getModal("deleteTaskConfirmModal").open();
    // TODO if (!modalRes) {
    // TODO     return;
    // TODO }
    // TODO try {
    // TODO     await client.mutate({
    // TODO         mutation: Mutation_DeleteTask,
    // TODO         variables: {
    // TODO             input: {
    // TODO                 uuid: task.uuid,
    // TODO             },
    // TODO         },
    // TODO     });
    // TODO     // closeTaskDetails(); TODO?
    // TODO } catch (error) {
    // TODO     console.error(error);
    // TODO }
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

export async function getWorkspaceBoard(
    uuid: string
): Promise<WorkspaceBoard> {
    return await getWithCredentialsJson<WorkspaceBoard>(
        `/workspace/workspace-board/${uuid}`
    );
}

export async function getWorkspaces(): Promise<Workspace[]> {
    return await getWithCredentialsJson<Workspace[]>(
        `/workspace/user/workspaces/`
    );
}

export async function getWorkspace(uuid: string): Promise<Workspace> {
    return await getWithCredentialsJson<Workspace>(
        `/workspace/workspace/${uuid}`
    );
}

export async function getTask(uuid: string): Promise<Task> {
    return await getWithCredentialsJson<Task>(`/workspace/task/${uuid}`);
}

export async function getArchivedWorkspaceBoards(
    workspace_uuid: string
): Promise<WorkspaceBoard[]> {
    return await getWithCredentialsJson<WorkspaceBoard[]>(
        `/workspace/workspace/${workspace_uuid}/workspace-boards-archived/`
    );
}
