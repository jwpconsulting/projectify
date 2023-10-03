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
import type { CreateTask, Task, WorkspaceUser } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";
// Task CRUD
// Create
interface CreateUpdateTaskData {
    title: string;
    description: string | undefined;
    labels: string[];
    assignee: string | null;
    workspace_board_section: string;
    // TODO dueDate plz
    deadline?: string;
}
export async function createTask(
    createTask: CreateTask,
    repositoryContext?: RepositoryContext
): Promise<Task> {
    const data: CreateUpdateTaskData = {
        title: createTask.title,
        description: createTask.description,
        labels: createTask.labels.map((label) => label.uuid),
        // TODO: Should the API just accept a missing value here?
        assignee: createTask.assignee?.uuid ?? null,
        workspace_board_section: createTask.workspace_board_section.uuid,
        deadline: createTask.deadline ?? undefined,
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
    repositoryContext?: RepositoryContext
): Promise<Task> {
    return await getWithCredentialsJson<Task>(
        `/workspace/task/${uuid}`,
        repositoryContext
    );
}

// Update
export async function updateTask(
    task: Task,
    labels: string[],
    workspaceUser: WorkspaceUser | undefined,
    repositoryContext?: RepositoryContext
): Promise<Task> {
    const { uuid: workspaceBoardSectionUuid } = unwrap(
        task.workspace_board_section,
        "Expected workspace_board_section"
    );
    const { uuid } = task;
    const data: CreateUpdateTaskData = {
        title: task.title,
        description: task.description ?? undefined,
        // XXX
        // Ideally, the two following arguments would just be part of the Task
        labels,
        assignee: workspaceUser?.uuid ?? null,
        workspace_board_section: workspaceBoardSectionUuid,
        // TODO sub tasks
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
