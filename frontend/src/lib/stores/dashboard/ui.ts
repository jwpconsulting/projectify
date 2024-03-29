// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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

const _selectedProjectUuids = persisted<Map<string, string>>(
    "selected-project-uuid",
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
export const selectedProjectUuids = readonly(_selectedProjectUuids);
export function selectProjectUuid(workspaceUuid: string, projectUuid: string) {
    _selectedProjectUuids.update(($selectedProjectUuids) => {
        $selectedProjectUuids.set(workspaceUuid, projectUuid);
        return $selectedProjectUuids;
    });
}

const _projectExpandOpen = persisted("board-expand-open", true);
export const projectExpandOpen = readonly(_projectExpandOpen);
export function toggleProjectExpandOpen() {
    _projectExpandOpen.update((state) => !state);
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

const _sectionClosed = persisted("section-closed", new Set<string>(), {
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
});
export const sectionClosed = readonly(_sectionClosed);

export function toggleSectionOpen(sectionUuid: string) {
    _sectionClosed.update(($sectionClosed) => {
        if ($sectionClosed.has(sectionUuid)) {
            $sectionClosed.delete(sectionUuid);
        } else {
            $sectionClosed.add(sectionUuid);
        }
        return $sectionClosed;
    });
}

// Adjust this if the dashboard URLs ever change
const showFilterRouteIds = ["/(platform)/dashboard/project/[projectUuid]"];

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
