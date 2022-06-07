import {
    Mutation_MoveTaskAfter,
    Mutation_DeleteTask,
} from "./../graphql/operations";
import { goto } from "$app/navigation";
import { encodeUUID } from "$lib/utils/encoders";
import Fuse from "fuse.js";
import { writable, get } from "svelte/store";
import { client } from "$lib/graphql/client";
import { getModal } from "$lib/components/dialogModal.svelte";

export const drawerModalOpen = writable(false);
export const currentWorkspaceUUID = writable<string | null>(null);
export const currentBoardUUID = writable<string | null>(null);
export const currenTaskDetailsUUID = writable<string | null>(null);
export const newTaskSectionUUID = writable<string | null>(null);
export const currentBoardSections = writable([]);

export function openNewTask(sectionUUID: string): void {
    drawerModalOpen.set(true);
    newTaskSectionUUID.set(sectionUUID);
    currenTaskDetailsUUID.set(null);
}
export function openTaskDetails(
    taskUUID: string,
    subView: string = null
): void {
    drawerModalOpen.set(true);
    currenTaskDetailsUUID.set(taskUUID);

    const workspaceUUID = get(currentWorkspaceUUID);
    const boardUUID = get(currentBoardUUID);

    gotoDashboard(workspaceUUID, boardUUID, taskUUID, subView);
}
export function closeTaskDetails(): void {
    drawerModalOpen.set(false);
    currenTaskDetailsUUID.set(null);

    const workspaceUUID = get(currentWorkspaceUUID);
    const boardUUID = get(currentBoardUUID);

    gotoDashboard(workspaceUUID, boardUUID, null);
}

export function getDashboardURL(
    workspaceUUID: string = null,
    boardUUID: string = null,
    taskUUID: string = null,
    subView: string = null
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
    workspaceUUID: string = null,
    boardUUID: string = null,
    taskUUID: string = null,
    subView: string = null
): void {
    const url = getDashboardURL(workspaceUUID, boardUUID, taskUUID, subView);
    const curURL = getDashboardURL(
        get(currentWorkspaceUUID),
        get(currentBoardUUID),
        get(currenTaskDetailsUUID),
        subView
    );

    console.log(url);
    console.log(curURL);
    // if (url == curURL) {
    //     return;
    // }
    console.log("goto utr");

    goto(url);
}

export function copyDashboardURL(
    workspaceUUID: string = null,
    boardUUID: string = null,
    taskUUID: string = null
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

export const currentWorkspaceLabels = writable([]);

export function filterSectionsTasks(
    sections: any[],
    labels: any[],
    assegnee: any
): any[] {
    if (labels.length) {
        const labelUUIDs = {};

        labels.forEach((l) => {
            labelUUIDs[l.uuid] = true;
        });

        sections = sections.map((section) => {
            const tasks = section.tasks.filter((task) => {
                return task.labels.findIndex((l) => labelUUIDs[l.uuid]) >= 0;
            });

            return {
                ...section,
                tasks,
                totalTasksCount: section.tasks.length,
            };
        });
    }

    if (assegnee) {
        sections = sections.map((section) => {
            const tasks = section.tasks.filter((task) => {
                if (assegnee === "unassigned") {
                    return !task.assignee;
                } else {
                    return task.assignee?.email === assegnee.email;
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

export function searchTasks(sections: any[], searchText: string): any[] {
    let tasks = [];

    sections.forEach((section) => {
        tasks = tasks.concat(section.tasks);
    });

    const searchEngine = new Fuse(tasks, {
        keys: ["title"],
        threshold: 0.3,
    });

    tasks = searchEngine.search(searchText).map((res) => res.item);

    return tasks;
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

export async function deleteTask(task, section): Promise<void> {
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
            update(cache, { data }) {
                const sectionUUID = section.uuid;
                const cacheId = `WorkspaceBoardSection:${sectionUUID}`;

                cache.modify({
                    id: cacheId,
                    fields: {
                        tasks(list = []) {
                            return list.filter(
                                (it) => it.__ref != `Task:${task.uuid}`
                            );
                        },
                    },
                });
            },
        });

        closeTaskDetails();
    } catch (error) {
        console.error(error);
    }
}
