import { writable } from "svelte/store";

import { goto } from "$app/navigation";
import { getDashboardWorkspaceBoardUrl, getDashboardTaskUrl } from "$lib/urls";
import { get } from "svelte/store";

import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard/workspaceBoard";

export const loading = writable<boolean>(false);

export function copyDashboardURL(
    workspaceBoardUuid: string,
    taskUuid: string | null = null
): void {
    const path = taskUuid
        ? getDashboardTaskUrl(workspaceBoardUuid, taskUuid, "details")
        : getDashboardWorkspaceBoardUrl(workspaceBoardUuid);
    const url = `${location.protocol}//${location.host}${path}`;
    navigator.clipboard.writeText(url);
}

export function pushTashUuidtoPath() {
    const boardUuid = get(currentWorkspaceBoardUuid);
    if (!boardUuid) {
        throw new Error("Expected boardUuid");
    }
    goto(getDashboardWorkspaceBoardUrl(boardUuid));
}

export async function setAndNavigateWorkspaceBoard(uuid: string) {
    currentWorkspaceBoardUuid.set(uuid);
    goto(getDashboardWorkspaceBoardUrl(uuid));
}

export const userExpandOpen = writable<boolean>(false);
export function toggleUserExpandOpen() {
    userExpandOpen.update((state) => !state);
}
export const labelExpandOpen = writable<boolean>(false);
export function toggleLabelDropdownClosedNavOpen() {
    labelExpandOpen.update((state) => !state);
}

export const sideNavOpen = writable<boolean>(false);
export function toggleSideNavOpen() {
    sideNavOpen.update(($sideNavOpen) => !$sideNavOpen);
}

export const workspaceBoardSectionClosed = writable<Set<string>>(new Set());
export function toggleWorkspaceBoardSectionOpen(
    workspaceBoardSectionUuid: string
) {
    workspaceBoardSectionClosed.update(($workspaceBoardSectionClosed) => {
        if ($workspaceBoardSectionClosed.has(workspaceBoardSectionUuid)) {
            $workspaceBoardSectionClosed.delete(workspaceBoardSectionUuid);
        } else {
            $workspaceBoardSectionClosed.add(workspaceBoardSectionUuid);
        }
        return $workspaceBoardSectionClosed;
    });
}
