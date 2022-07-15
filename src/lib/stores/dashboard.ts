import {
    Mutation_MoveTaskAfter,
    Mutation_DeleteTask,
    Mutation_AssignTask,
} from "./../graphql/operations";
import { goto } from "$app/navigation";
import { encodeUUID } from "$lib/utils/encoders";
import Fuse from "fuse.js";
import lodash from "lodash";
import { writable, get } from "svelte/store";
import { client } from "$lib/graphql/client";
import { getModal } from "$lib/components/dialogModal.svelte";
import type {
    Label,
    Task,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types";

export const drawerModalOpen = writable(false);
export const currentWorkspaceUUID = writable<string | null>(null);
export const currentBoardUUID = writable<string | null>(null);
export const currentTaskDetailsUUID = writable<string | null>(null);
export const newTaskSectionUUID = writable<string | null>(null);
export const currentBoardSections = writable<WorkspaceBoardSection[]>([]);

export const fuseSearchThreshold = 0.3;

export function openNewTask(sectionUUID: string): void {
    drawerModalOpen.set(true);
    newTaskSectionUUID.set(sectionUUID);
    currentTaskDetailsUUID.set(null);
}
export function openTaskDetails(
    taskUUID: string,
    subView: string | null = null
): void {
    drawerModalOpen.set(true);
    currentTaskDetailsUUID.set(taskUUID);

    const workspaceUUID = get(currentWorkspaceUUID);
    const boardUUID = get(currentBoardUUID);

    gotoDashboard(workspaceUUID, boardUUID, taskUUID, subView);
}
export function closeTaskDetails(): void {
    drawerModalOpen.set(false);
    currentTaskDetailsUUID.set(null);

    const workspaceUUID = get(currentWorkspaceUUID);
    const boardUUID = get(currentBoardUUID);

    gotoDashboard(workspaceUUID, boardUUID, null);
}

export function getDashboardURL(
    workspaceUUID: string | null = null,
    boardUUID: string | null = null,
    taskUUID: string | null = null,
    subView: string | null = null
): string {
    workspaceUUID = workspaceUUID ? encodeUUID(workspaceUUID) : null;
    boardUUID = boardUUID ? encodeUUID(boardUUID) : null;
    taskUUID = taskUUID ? encodeUUID(taskUUID) : null;

    let url = "/dashboard/";

    if (workspaceUUID) {
        url += workspaceUUID;
        if (boardUUID) {
            url += "/" + boardUUID;
            if (taskUUID) {
                url += "/" + taskUUID;
                if (subView) {
                    url += "/" + subView;
                }
            }
        }
    }

    return url;
}

export function gotoDashboard(
    workspaceUUID: string | null = null,
    boardUUID: string | null = null,
    taskUUID: string | null = null,
    subView: string | null = null
): void {
    const url = getDashboardURL(workspaceUUID, boardUUID, taskUUID, subView);
    goto(url);
}

export function copyDashboardURL(
    workspaceUUID: string | null = null,
    boardUUID: string | null = null,
    taskUUID: string | null = null
): void {
    let url = getDashboardURL(workspaceUUID, boardUUID, taskUUID);
    url = `${location.protocol}//${location.host}${url}`;
    navigator.clipboard.writeText(url);
}

export function pushTashUUIDtoPath(uuid: string): void {
    const workspaceUUID = get(currentWorkspaceUUID);
    const boardUUID = get(currentBoardUUID);
    if (workspaceUUID && boardUUID) {
        gotoDashboard(workspaceUUID, boardUUID, uuid);
    }
}

export const currentWorkspaceLabels = writable<Label[]>([]);

export function filterSectionsTasks(
    sections: WorkspaceBoardSection[],
    labels: Label[],
    assignee: WorkspaceUser | "unassigned" | null
): WorkspaceBoardSection[] {
    if (labels.length) {
        const labelUuids = new Map<string, boolean>();

        labels.forEach((l) => {
            labelUuids.set(l.uuid, true);
        });

        sections = sections.map((section) => {
            const sectionTasks = section.tasks ? section.tasks : [];
            const tasks = sectionTasks.filter((task: Task) => {
                return (
                    task.labels.findIndex((l: Label) =>
                        labelUuids.get(l.uuid) ? true : false
                    ) >= 0
                );
            });

            return {
                ...section,
                tasks,
            };
        });
    }

    if (assignee) {
        sections = sections.map((section) => {
            const sectionTasks = section.tasks ? section.tasks : [];
            const tasks = sectionTasks.filter((task: Task) => {
                if (assignee === "unassigned") {
                    return !task.assignee;
                } else {
                    return task.assignee?.user.email === assignee.user.email;
                }
            });

            return {
                ...section,
                tasks,
            };
        });
    }

    return sections;
}

export function searchTasks(
    sections: WorkspaceBoardSection[],
    searchText: string
): Task[] {
    const tasks: Task[] = lodash.flatten(
        sections.map((section) => (section.tasks ? section.tasks : []))
    );

    const searchEngine: Fuse<Task> = new Fuse(tasks, {
        keys: ["title"],
        threshold: fuseSearchThreshold,
    });

    return searchEngine
        .search(searchText)
        .map((res: Fuse.FuseResult<Task>) => res.item);
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
    const modalRes = await getModal("deleteTaskConfirmModal").open();

    if (!modalRes) {
        return;
    }

    try {
        await client.mutate({
            mutation: Mutation_DeleteTask,
            variables: {
                input: {
                    uuid: task.uuid,
                },
            },
        });

        closeTaskDetails();
    } catch (error) {
        console.error(error);
    }
}

export async function assignUserToTask(
    userEmail: string | null,
    taskUUID: string
): Promise<void> {
    try {
        await client.mutate({
            mutation: Mutation_AssignTask,
            variables: {
                input: {
                    uuid: taskUUID,
                    email: userEmail,
                },
            },
        });
    } catch (error) {
        console.error(error);
    }
}
