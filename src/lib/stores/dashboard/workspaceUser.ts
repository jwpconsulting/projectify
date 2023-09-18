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
import type { TasksPerUser } from "$lib/types/ui";
import type {
    Workspace,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";

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
export const createWorkspaceUserSearch = () =>
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

type CurrentTasksPerUser = Readable<TasksPerUser>;

export function createTasksPerUser(
    currentWorkspaceBoardSections: Readable<WorkspaceBoardSection[]>
): CurrentTasksPerUser {
    return derived<Readable<WorkspaceBoardSection[]>, TasksPerUser>(
        currentWorkspaceBoardSections,
        ($currentWorkspaceBoardSections, set) => {
            const userCounts = new Map<string, number>();
            let unassignedCounts = 0;
            $currentWorkspaceBoardSections.forEach((section) => {
                if (!section.tasks) {
                    return;
                }
                section.tasks.forEach((task) => {
                    if (task.assignee) {
                        const uuid = task.assignee.uuid;
                        const count = userCounts.get(uuid);
                        if (count) {
                            userCounts.set(uuid, count + 1);
                        } else {
                            userCounts.set(uuid, 1);
                        }
                    } else {
                        unassignedCounts = unassignedCounts + 1;
                    }
                });
            });
            const counts: TasksPerUser = {
                unassigned: unassignedCounts,
                assigned: userCounts,
            };
            set(counts);
        },
        { unassigned: 0, assigned: new Map<string, number>() }
    );
}
