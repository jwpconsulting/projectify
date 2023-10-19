import type { FetchResult } from "@apollo/client/core";

import { client } from "$lib/graphql/client";
import {
    Mutation_AssignLabel,
    Mutation_AssignTask,
    Mutation_MoveTaskAfter,
    Mutation_DeleteTask,
} from "$lib/graphql/operations";
import {
    putWithCredentialsJson,
    getWithCredentialsJson,
    postWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    CreateUpdateSubTask,
    CreateUpdateTask,
    Label,
    Task,
    TaskWithWorkspace,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";

// Task CRUD
// Create
interface CreateUpdateTaskData {
    title: string;
    description?: string;
    // TODO this has to be optional in the backend -> undefined means unset
    // labels
    labels: Label[];
    // TODO this has to be optional in the backend -> undefined means unset
    // assignee
    assignee: WorkspaceUser | null;
    workspace_board_section: WorkspaceBoardSection;
    // TODO dueDate plz
    deadline?: string;
    sub_tasks?: CreateUpdateSubTask[];
}
// TODO change me to accept CreateOrUpdateTaskData directly
export async function createTask(
    createTask: CreateUpdateTask,
    repositoryContext: RepositoryContext
): Promise<Task> {
    const data: CreateUpdateTaskData = {
        ...createTask,
        // TODO: Should the API just accept a missing value here?
        assignee: createTask.assignee ?? null,
    };
    return await postWithCredentialsJson<Task>(
        "/workspace/task",
        data,
        repositoryContext
    );
}

// Read
export async function getTask(
    uuid: string,
    repositoryContext: RepositoryContext
): Promise<TaskWithWorkspace> {
    return await getWithCredentialsJson<TaskWithWorkspace>(
        `/workspace/task/${uuid}`,
        repositoryContext
    );
}

// Update
// TODO change me to accept CreateOrUpdateTaskData directly
// Then we don't have to pass task, labels, ws user separately
// This is possible now because the API accepts a whole task object,
// incl. labels and so on
export async function updateTask(
    task: Task & { workspace_board_section: WorkspaceBoardSection },
    // XXX please move the following three arguments back into the top task
    // argument
    labels: Label[],
    workspaceUser: WorkspaceUser | undefined,
    subTasks: CreateUpdateSubTask[] | undefined,
    repositoryContext: RepositoryContext
): Promise<Task> {
    const { uuid } = task;
    const data: CreateUpdateTaskData = {
        title: task.title,
        description: task.description ?? undefined,
        // XXX
        // Ideally, the two following arguments would just be part of the Task
        labels,
        // TODO
        // Please be undefined, not null
        // Might have to check if the backend already accepts undefined as
        // unassign
        assignee: workspaceUser ?? null,
        workspace_board_section: task.workspace_board_section,
        sub_tasks: subTasks,
    };
    return await putWithCredentialsJson<Task>(
        `/workspace/task/${uuid}`,
        data,
        repositoryContext
    );
}

// TODO now that we have updateTask feature complete, we can remove
// assignUser / assignLabel Justus 2023-10-03
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
): Promise<Task> {
    const result: FetchResult<{ assignLabel: Task }> = await client.mutate({
        mutation: Mutation_AssignLabel,
        variables: {
            input: {
                taskUuid: task.uuid,
                labelUuid,
                assigned,
            },
        },
    });
    if (!result.data) {
        throw new Error("Expected result.data");
    }
    return result.data.assignLabel;
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
