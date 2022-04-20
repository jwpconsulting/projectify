import { goto } from "$app/navigation";
import { encodeUUID } from "$lib/utils/encoders";
import Fuse from "fuse.js";
import { writable, get } from "svelte/store";

export const drawerModalOpen = writable(false);
export const currentWorkspaceUUID = writable<string | null>(null);
export const currentBoardUUID = writable<string | null>(null);
export const currenTaskDetailsUUID = writable<string | null>(null);
export const newTaskSectionUUID = writable<string | null>(null);

export function openNewTask(sectionUUID: string): void {
    drawerModalOpen.set(true);
    newTaskSectionUUID.set(sectionUUID);
    currenTaskDetailsUUID.set(null);
}
export function openTaskDetails(taskUUID: string): void {
    drawerModalOpen.set(true);
    currenTaskDetailsUUID.set(taskUUID);

    const workspaceUUID = get(currentWorkspaceUUID);
    const boardUUID = get(currentBoardUUID);

    gotoDashboard(workspaceUUID, boardUUID, taskUUID);
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
    taskUUID: string = null
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
            }
        }
    }

    return url;
}

export function gotoDashboard(
    workspaceUUID: string = null,
    boardUUID: string = null,
    taskUUID: string = null
): void {
    const url = getDashboardURL(workspaceUUID, boardUUID, taskUUID);
    goto(url);
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
                return task.assignee?.email === assegnee.email;
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
    });

    tasks = searchEngine.search(searchText).map((res) => res.item);

    return tasks;
}
