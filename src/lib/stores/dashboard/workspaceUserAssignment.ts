import { writable } from "svelte/store";

import { assignUserToTask } from "$lib/repository/workspace";
import type { WorkspaceUserFilter } from "$lib/types/stores";
import type {
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type { Task } from "$lib/types/workspace";

export async function assignWorkspaceUser(
    task: Task,
    selection: WorkspaceUserSelectionInput
) {
    if (selection.kind === "unassigned") {
        await assignUserToTask(null, task.uuid);
    } else if (selection.kind === "allWorkspaceUsers") {
        throw new Error("Unsupported");
    } else {
        await assignUserToTask(selection.workspaceUser.user.email, task.uuid);
    }
}

export function createWorkspaceUserSearchStore(task: Task) {
    const selected: WorkspaceUserSelection = task.assignee
        ? {
              kind: "workspaceUsers",
              workspaceUserUuids: new Set([task.assignee.uuid]),
          }
        : {
              kind: "unassigned",
          };
    const workspaceUserFilter: WorkspaceUserFilter = {
        async select(selection: WorkspaceUserSelectionInput) {
            await assignWorkspaceUser(task, selection);
        },
        deselect: console.error,
        selected: writable<WorkspaceUserSelection>(selected),
    };
    return workspaceUserFilter;
}
