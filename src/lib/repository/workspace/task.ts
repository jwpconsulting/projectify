import type { ApolloQueryResult } from "@apollo/client/core";

import { client } from "$lib/graphql/client";
import {
    Mutation_AddTask,
    Mutation_AssignLabel,
    Mutation_AssignTask,
    Mutation_MoveTaskAfter,
    Mutation_UpdateTask,
    Mutation_DeleteTask,
} from "$lib/graphql/operations";
import type { CreateTask, Task } from "$lib/types/workspace";
// Task CRUD
// Create
export async function createTask(createTask: CreateTask): Promise<Task> {
    const {
        data: { addTask: task },
    } = (await client.mutate({
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
    })) as ApolloQueryResult<{ addTask: Task }>;
    return task;
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
