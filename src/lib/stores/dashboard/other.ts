import { writable } from "svelte/store";

import { goto } from "$app/navigation";
import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard/workspaceBoard";

export const loading = writable<boolean>(false);

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
