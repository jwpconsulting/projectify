import { writable } from "svelte/store";

import { internallyWritable } from "$lib/stores/util";

// TODO loading needed?
export const loading = writable<boolean>(false);

const { priv: _userExpandOpen, pub: userExpandOpen } =
    internallyWritable(false);
export function toggleUserExpandOpen() {
    _userExpandOpen.update((state) => !state);
}
export { userExpandOpen };

const { priv: _labelExpandOpen, pub: labelExpandOpen } =
    internallyWritable(false);
export function toggleLabelDropdownClosedNavOpen() {
    _labelExpandOpen.update((state) => !state);
}
export { labelExpandOpen };

const { priv: _sideNavOpen, pub: sideNavOpen } = internallyWritable(true);
export function toggleSideNavOpen() {
    _sideNavOpen.update(($sideNavOpen) => !$sideNavOpen);
}
export { sideNavOpen };

const {
    priv: _workspaceBoardSectionClosed,
    pub: workspaceBoardSectionClosed,
} = internallyWritable<Set<string>>(new Set());
export function toggleWorkspaceBoardSectionOpen(
    workspaceBoardSectionUuid: string
) {
    _workspaceBoardSectionClosed.update(($workspaceBoardSectionClosed) => {
        if ($workspaceBoardSectionClosed.has(workspaceBoardSectionUuid)) {
            $workspaceBoardSectionClosed.delete(workspaceBoardSectionUuid);
        } else {
            $workspaceBoardSectionClosed.add(workspaceBoardSectionUuid);
        }
        return $workspaceBoardSectionClosed;
    });
}
export { workspaceBoardSectionClosed };
