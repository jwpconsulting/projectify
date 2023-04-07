import {
    Mutation_AddLabelMutation,
    Mutation_AddWorkspaceBoardSection,
    Mutation_ArchiveWorkspaceBoard,
    Mutation_AssignTask,
    Mutation_DeleteLabelMutation,
    Mutation_MoveTaskAfter,
    Mutation_UpdateLabelMutation,
} from "$lib/graphql/operations";
import type {
    CreateWorkspaceBoardSection,
    Label,
    Task,
    Workspace,
    WorkspaceBoard,
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

// These methods find refuge from SelectWorkspaceBoard.svelte here
export async function updateWorkspaceBoard() {
    // TODO modal
    // await client.mutate({
    //     mutation: Mutation_UpdateWorkspaceBoard,
    //     variables: {
    //         input: {
    //             uuid: workspaceBoard.uuid,
    //             title: modalRes.outputs.title,
    //             deadline: modalRes.outputs.deadline,
    //             description: "",
    //         },
    //     },
    // });
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
