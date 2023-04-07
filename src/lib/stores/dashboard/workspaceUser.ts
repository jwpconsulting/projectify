import Fuse from "fuse.js";
import { writable, derived } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { WorkspaceUser } from "$lib/types/workspace";
import { fuseSearchThreshold } from "$lib/config";
import type {
    WorkspaceUserSelectionInput,
    WorkspaceUserSelection,
} from "$lib/types/ui";

// WorkspaceUser Search and Selection
export const currentWorkspaceUsers = derived<
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

export const workspaceUserSearch = writable<string>("");

function searchWorkspaceUsers(
    workspaceUsers: WorkspaceUser[],
    searchInput: string
) {
    if (searchInput === "") {
        return workspaceUsers;
    }
    const searchEngine = new Fuse(workspaceUsers, {
        keys: ["user.email", "user.full_name"],
        threshold: fuseSearchThreshold,
        shouldSort: false,
    });
    const result = searchEngine.search(searchInput);
    return result.map((res: Fuse.FuseResult<WorkspaceUser>) => res.item);
}

export const workspaceUserSearchResults = derived<
    [typeof currentWorkspaceUsers, typeof workspaceUserSearch],
    WorkspaceUser[]
>(
    [currentWorkspaceUsers, workspaceUserSearch],
    ([$currentWorkspaceUsers, $workspaceUserSearch], set) => {
        set(
            searchWorkspaceUsers($currentWorkspaceUsers, $workspaceUserSearch)
        );
    },
    []
);

export const selectedWorkspaceUser = writable<WorkspaceUserSelection>({
    kind: "allWorkspaceUsers",
});

export function selectWorkspaceUser(selection: WorkspaceUserSelectionInput) {
    selectedWorkspaceUser.update(
        (currentSelection: WorkspaceUserSelection) => {
            if (selection.kind === "allWorkspaceUsers") {
                return { kind: "allWorkspaceUsers" };
            } else if (selection.kind === "unassigned") {
                if (currentSelection.kind === "unassigned") {
                    return { kind: "allWorkspaceUsers" };
                } else {
                    return { kind: "unassigned" };
                }
            } else {
                const selectionUuid = selection.workspaceUser.uuid;
                if (currentSelection.kind === "workspaceUsers") {
                    currentSelection.workspaceUserUuids.add(selectionUuid);
                    return currentSelection;
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
    selectedWorkspaceUser.update(
        (currentSelection: WorkspaceUserSelection) => {
            if (selection.kind === "allWorkspaceUsers") {
                return { kind: "allWorkspaceUsers" };
            } else if (selection.kind === "unassigned") {
                if (currentSelection.kind === "unassigned") {
                    return { kind: "allWorkspaceUsers" };
                } else {
                    return { kind: "unassigned" };
                }
            } else {
                const selectionUuid = selection.workspaceUser.uuid;
                if (currentSelection.kind === "workspaceUsers") {
                    currentSelection.workspaceUserUuids.delete(selectionUuid);
                    if (currentSelection.workspaceUserUuids.size === 0) {
                        return { kind: "allWorkspaceUsers" };
                    } else {
                        return currentSelection;
                    }
                } else {
                    return { kind: "allWorkspaceUsers" };
                }
            }
        }
    );
}
