import { readonly } from "svelte/store";
import { persisted } from "svelte-local-storage-store";

const _boardExpandOpen = persisted("board-expand-open", true);
export const boardExpandOpen = readonly(_boardExpandOpen);
export function toggleBoardExpandOpen() {
    _boardExpandOpen.update((state) => !state);
}

const _userExpandOpen = persisted("user-expand-open", true);
export const userExpandOpen = readonly(_userExpandOpen);
export function toggleUserExpandOpen() {
    _userExpandOpen.update((state) => !state);
}

const _labelExpandOpen = persisted("label-expand-open", true);
export const labelExpandOpen = readonly(_labelExpandOpen);
export function toggleLabelDropdownClosedNavOpen() {
    _labelExpandOpen.update((state) => !state);
}

const _sideNavOpen = persisted("side-nav-open", true);
export const sideNavOpen = readonly(_sideNavOpen);
export function toggleSideNavOpen() {
    _sideNavOpen.update((state) => !state);
}

const _workspaceBoardSectionClosed = persisted(
    "workspace-board-section-closed",
    new Set<string>(),
    {
        serializer: {
            // XXX Using json.parse, maybe a security problem?
            parse(value: string): Set<string> {
                const values = JSON.parse(value) as string[];
                try {
                    return new Set(values);
                } catch {
                    return new Set();
                }
            },
            stringify(set: Set<string>): string {
                const values: string[] = [...set];
                return JSON.stringify(values);
            },
        },
    }
);
export const workspaceBoardSectionClosed = readonly(
    _workspaceBoardSectionClosed
);

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
