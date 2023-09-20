/*
 * Workspace user related store
 * Following use cases:
 *
 * - Selecting a user to be assigned to task (workspaceUserAssignment)
 * - Filtering tasks inside a ws board by ws user
 * (workspaceUserFilter)
 * Before I wrote these two things to be the same, even though that meant
 * unnecessarily shoehorning unrelated features into the same thing
 */
import { derived, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import { searchAmong } from "$lib/stores/util";
import type { SearchInput } from "$lib/types/base";
import type { Workspace, WorkspaceUser } from "$lib/types/workspace";

// WorkspaceUser Search and Selection
type CurrentWorkspaceUsers = Readable<WorkspaceUser[]>;

export const currentWorkspaceUsers: CurrentWorkspaceUsers = derived<
    typeof currentWorkspace,
    WorkspaceUser[]
    // Derived stores are initialized with undefined
>(
    currentWorkspace,
    ($currentWorkspace: Workspace | undefined, set) => {
        if (!$currentWorkspace) {
            return;
        }
        if (!$currentWorkspace.workspace_users) {
            throw new Error("Expected $currentWorkspace.workspace_users");
        }
        set($currentWorkspace.workspace_users);
    },
    []
);

export type WorkspaceUserSearch = Writable<SearchInput>;
export const createWorkspaceUserFilter = () =>
    writable<SearchInput>(undefined);

function searchWorkspaceUsers(
    workspaceUsers: WorkspaceUser[],
    searchInput: SearchInput
) {
    return searchAmong(
        ["user.email", "user.full_name"],
        workspaceUsers,
        searchInput
    );
}

export type WorkspaceUserSearchResults = Readable<WorkspaceUser[]>;

export function createWorkspaceUserSearchResults(
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
