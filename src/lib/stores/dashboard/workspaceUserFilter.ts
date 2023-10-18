/*
 * Filter used to filter tasks by workspace users
 */
import { derived, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

import { internallyWritable, searchAmong } from "../util";

import { currentWorkspaceUsers } from "$lib/stores/dashboard/workspaceUser";
import type { CurrentWorkspaceUsers } from "$lib/stores/dashboard/workspaceUser";
import type { SearchInput } from "$lib/types/base";
import type {
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type { WorkspaceUser } from "$lib/types/workspace";

const { priv: _selectedWorkspaceUser, pub: selectedWorkspaceUser } =
    internallyWritable<WorkspaceUserSelection>({
        kind: "allWorkspaceUsers",
    });
export { selectedWorkspaceUser };

type WorkspaceUserSearch = Writable<SearchInput>;
const createWorkspaceUserFilter = () => writable<SearchInput>(undefined);

export function searchWorkspaceUsers(
    workspaceUsers: WorkspaceUser[],
    searchInput: SearchInput
) {
    return searchAmong(
        ["user.email", "user.full_name"],
        workspaceUsers,
        searchInput
    );
}

type WorkspaceUserSearchResults = Readable<WorkspaceUser[]>;

function createWorkspaceUserSearchResults(
    currentWorkspaceUsers: CurrentWorkspaceUsers,
    workspaceUserSearch: WorkspaceUserSearch
): WorkspaceUserSearchResults {
    return derived<
        [typeof currentWorkspaceUsers, typeof workspaceUserSearch],
        WorkspaceUser[]
    >(
        [currentWorkspaceUsers, workspaceUserSearch],
        ([$currentWorkspaceUsers, $workspaceUserSearch], set) => {
            set(
                searchWorkspaceUsers(
                    $currentWorkspaceUsers,
                    $workspaceUserSearch
                )
            );
        },
        []
    );
}

export const workspaceUserSearch: WorkspaceUserSearch =
    createWorkspaceUserFilter();

export const workspaceUserSearchResults: WorkspaceUserSearchResults =
    createWorkspaceUserSearchResults(
        currentWorkspaceUsers,
        workspaceUserSearch
    );

export function filterByWorkspaceUser(selection: WorkspaceUserSelectionInput) {
    _selectedWorkspaceUser.update(
        ($selectedWorkspaceUser: WorkspaceUserSelection) => {
            if (selection.kind === "allWorkspaceUsers") {
                return { kind: "allWorkspaceUsers" };
            } else if (selection.kind === "unassigned") {
                if ($selectedWorkspaceUser.kind === "unassigned") {
                    return { kind: "allWorkspaceUsers" };
                } else {
                    return { kind: "unassigned" };
                }
            } else {
                const selectionUuid = selection.workspaceUser.uuid;
                if ($selectedWorkspaceUser.kind === "workspaceUsers") {
                    $selectedWorkspaceUser.workspaceUserUuids.add(
                        selectionUuid
                    );
                    return $selectedWorkspaceUser;
                } else {
                    const workspaceUserUuids = new Set<string>();
                    workspaceUserUuids.add(selectionUuid);
                    return { kind: "workspaceUsers", workspaceUserUuids };
                }
            }
        }
    );
}

export function unfilterByWorkspaceUser(
    selection: WorkspaceUserSelectionInput
) {
    _selectedWorkspaceUser.update(
        ($selectedWorkspaceUser: WorkspaceUserSelection) => {
            if (selection.kind === "allWorkspaceUsers") {
                return { kind: "allWorkspaceUsers" };
            } else if (selection.kind === "unassigned") {
                if ($selectedWorkspaceUser.kind === "unassigned") {
                    return { kind: "allWorkspaceUsers" };
                } else {
                    return { kind: "unassigned" };
                }
            } else {
                const selectionUuid = selection.workspaceUser.uuid;
                if ($selectedWorkspaceUser.kind === "workspaceUsers") {
                    $selectedWorkspaceUser.workspaceUserUuids.delete(
                        selectionUuid
                    );
                    if ($selectedWorkspaceUser.workspaceUserUuids.size === 0) {
                        return { kind: "allWorkspaceUsers" };
                    } else {
                        return $selectedWorkspaceUser;
                    }
                } else {
                    return { kind: "allWorkspaceUsers" };
                }
            }
        }
    );
}
