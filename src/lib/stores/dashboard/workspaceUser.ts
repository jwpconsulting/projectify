import { derived, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import { internallyWritable, searchAmong } from "$lib/stores/util";
import type { SearchInput } from "$lib/types/base";
import type {
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type { WorkspaceUser } from "$lib/types/workspace";

// WorkspaceUser Search and Selection
type CurrentWorkspaceUsers = Readable<WorkspaceUser[]>;

export const currentWorkspaceUsers: CurrentWorkspaceUsers = derived<
    [typeof currentWorkspace],
    WorkspaceUser[]
>(
    [currentWorkspace],
    ([$currentWorkspace], set) => {
        if (!$currentWorkspace) {
            set([]);
            return;
        }
        if (!$currentWorkspace.workspace_users) {
            throw new Error("Expected $currentWorkspace.workspace_users");
        }
        set($currentWorkspace.workspace_users);
    },
    []
);

type WorkspaceUserSearch = Writable<SearchInput>;
const createWorkspaceUserSearch = () => writable<SearchInput>(undefined);

export const workspaceUserSearch: WorkspaceUserSearch =
    createWorkspaceUserSearch();

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

type WorkspaceUserSearchResults = Readable<WorkspaceUser[]>;

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

export const workspaceUserSearchResults: WorkspaceUserSearchResults =
    createWorkspaceUserSearchResults(
        currentWorkspaceUsers,
        workspaceUserSearch
    );

const { priv: _selectedWorkspaceUser, pub: selectedWorkspaceUser } =
    internallyWritable<WorkspaceUserSelection>({
        kind: "allWorkspaceUsers",
    });
export { selectedWorkspaceUser };

export function selectWorkspaceUser(selection: WorkspaceUserSelectionInput) {
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

export function deselectWorkspaceUser(selection: WorkspaceUserSelectionInput) {
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
