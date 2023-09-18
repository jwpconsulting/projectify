/*
 * Workspace user related store
 * Following use cases:
 *
 * - Selecting a user to be assigned to task (workspaceUserAssignment)
 * - Filtering tasks inside a ws board by ws user
 * (workspaceUserSearch)
 * Before I wrote these two things to be the same, even though that meant
 * unnecessarily shoehorning unrelated features into the same thing
 */
import { derived, readable, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

import { _selectedWorkspaceUser } from "./selectedWorkspaceUser";

import { assignUserToTask } from "$lib/repository/workspace";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import { currentWorkspaceBoardSections } from "$lib/stores/dashboard/workspaceBoardSection";
import { searchAmong } from "$lib/stores/util";
import type { SearchInput } from "$lib/types/base";
import type { WorkspaceUserSearchStore } from "$lib/types/stores";
import type {
    TasksPerUser,
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type {
    Task,
    Workspace,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";

// WorkspaceUser Search and Selection
type CurrentWorkspaceUsers = Readable<WorkspaceUser[]>;

const currentWorkspaceUsers: CurrentWorkspaceUsers = derived<
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

type WorkspaceUserSearch = Writable<SearchInput>;
const createWorkspaceUserSearch = () => writable<SearchInput>(undefined);

const workspaceUserSearch: WorkspaceUserSearch = createWorkspaceUserSearch();

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

const workspaceUserSearchResults: WorkspaceUserSearchResults =
    createWorkspaceUserSearchResults(
        currentWorkspaceUsers,
        workspaceUserSearch
    );

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

function deselectWorkspaceUser(selection: WorkspaceUserSelectionInput) {
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

export function createWorkspaceUserSearchStore(task: Task) {
    const workspaceUserSearch = createWorkspaceUserSearch();
    const selected: WorkspaceUserSelection = task.assignee
        ? {
              kind: "workspaceUsers",
              workspaceUserUuids: new Set([task.assignee.uuid]),
          }
        : {
              kind: "unassigned",
          };
    const workspaceUserSearchModule: WorkspaceUserSearchStore = {
        select: async (selection: WorkspaceUserSelectionInput) => {
            if (selection.kind === "unassigned") {
                await assignUserToTask(null, task.uuid);
            } else if (selection.kind === "allWorkspaceUsers") {
                throw new Error("Unsupported");
            } else {
                await assignUserToTask(
                    selection.workspaceUser.user.email,
                    task.uuid
                );
            }
        },
        deselect: console.error,
        selected: writable<WorkspaceUserSelection>(selected),
        // XXX find a way to postpone this, albeit useful, showing
        // the amount of tasks per users right from the beginning
        // will be more work
        tasksPerUser: readable<TasksPerUser>({
            unassigned: 0,
            assigned: new Map(),
        }),
        search: workspaceUserSearch,
        searchResults: createWorkspaceUserSearchResults(
            currentWorkspaceUsers,
            workspaceUserSearch
        ),
    };
    return workspaceUserSearchModule;
}

type CurrentTasksPerUser = Readable<TasksPerUser>;

function createTasksPerUser(
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

export const workspaceUserSearchModule: WorkspaceUserSearchStore = {
    select: selectWorkspaceUser,
    deselect: deselectWorkspaceUser,
    selected: _selectedWorkspaceUser,
    search: workspaceUserSearch,
    searchResults: workspaceUserSearchResults,
    tasksPerUser: createTasksPerUser(currentWorkspaceBoardSections),
};
