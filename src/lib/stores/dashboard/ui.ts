import { writable } from "svelte/store";

// TODO loading needed?
export const loading = writable<boolean>(false);

export const userExpandOpen = writable<boolean>(false);
export function toggleUserExpandOpen() {
    userExpandOpen.update((state) => !state);
}
export const labelExpandOpen = writable<boolean>(false);
export function toggleLabelDropdownClosedNavOpen() {
    labelExpandOpen.update((state) => !state);
}

export const sideNavOpen = writable<boolean>(true);
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
