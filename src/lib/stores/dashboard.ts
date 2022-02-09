import { goto } from "$app/navigation";
import { encodeUUID } from "$lib/utils/encoders";
import { writable } from "svelte/store";

export const drawerModalOpen = writable(false);
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
}
export function closeTaskDetails(): void {
    drawerModalOpen.set(false);
    currenTaskDetailsUUID.set(null);
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
