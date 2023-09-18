import { readable, writable } from "svelte/store";

import {
    createWorkspaceUserSearch,
    createWorkspaceUserSearchResults,
    currentWorkspaceUsers,
} from "./workspaceUser";

import { assignUserToTask } from "$lib/repository/workspace";
import type { WorkspaceUserSearchStore } from "$lib/types/stores";
import type {
    TasksPerUser,
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type { Task } from "$lib/types/workspace";

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
    const workspaceUserFilter: WorkspaceUserSearchStore = {
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
    return workspaceUserFilter;
}
