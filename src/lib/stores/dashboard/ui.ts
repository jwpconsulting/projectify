import { derived, readonly } from "svelte/store";
import { persisted } from "svelte-local-storage-store";

import { page } from "$app/stores";

/*
 * Store which workspace we have seen last.
 * When we fetch a workspace based on this uuid, we must invalidate it
 * on a 404 workspace not found
 */
const _selectedWorkspaceUuid = persisted<string | null>(
    "selected-workspace-uuid",
    null,
);
export const selectedWorkspaceUuid = readonly(_selectedWorkspaceUuid);
export function selectWorkspaceUuid(uuid: string) {
    _selectedWorkspaceUuid.set(uuid);
}
/*
 * Clear a selected workspace uuid, if it matches the uuid arg
 */
export function clearSelectedWorkspaceUuidIfMatch(uuid: string) {
    _selectedWorkspaceUuid.update(($uuid) => {
        if ($uuid === uuid) {
            return null;
        }
        return $uuid;
    });
}

const _selectedWorkspaceBoardUuids = persisted<Map<string, string>>(
    "selected-workspace-board-uuid",
    new Map(),
    {
        serializer: {
            // XXX Using json.parse, maybe a security problem?
            parse(value: string): Map<string, string> {
                const values = JSON.parse(value) as [string, string][];
                try {
                    return new Map(values);
                } catch {
                    return new Map();
                }
            },
            stringify(map: Map<string, string>): string {
                const values: [string, string][] = Array.from(map);
                return JSON.stringify(values);
            },
        },
    },
);
export const selectedWorkspaceBoardUuids = readonly(
    _selectedWorkspaceBoardUuids,
);
export function selectWorkspaceBoardUuid(
    workspaceUuid: string,
    workspaceBoardUuid: string,
) {
    _selectedWorkspaceBoardUuids.update(($selectedWorkspaceBoardUuids) => {
        $selectedWorkspaceBoardUuids.set(workspaceUuid, workspaceBoardUuid);
        return $selectedWorkspaceBoardUuids;
    });
}

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
// TODO rename toggleLabelExpandOpen
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
    },
);
export const workspaceBoardSectionClosed = readonly(
    _workspaceBoardSectionClosed,
);

export function toggleWorkspaceBoardSectionOpen(
    workspaceBoardSectionUuid: string,
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

// Adjust this if the dashboard URLs ever change
const showFilterRouteIds = [
    "/(platform)/dashboard/workspace-board/[workspaceBoardUuid]",
];

/*
 * showFilters is true only for pages for which we show the user
 * the filter user / label options
 */
export const showFilters = derived<typeof page, boolean>(
    page,
    ($page, set) => {
        const { route } = $page;
        const { id } = route;
        set(showFilterRouteIds.find((i) => i === id) !== undefined);
    },
    false,
);
