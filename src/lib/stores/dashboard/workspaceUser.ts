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
import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Workspace, WorkspaceUser } from "$lib/types/workspace";

export type CurrentWorkspaceUsers = Readable<WorkspaceUser[]>;

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
    [],
);
