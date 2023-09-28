import { derived, readonly, writable } from "svelte/store";

import type { WorkspaceUserAssignment } from "$lib/types/stores";
import type {
    WorkspaceUserAssignmentInput,
    WorkspaceUserAssignmentState,
} from "$lib/types/ui";
import type { Task, WorkspaceUser } from "$lib/types/workspace";

export function createWorkspaceUserAssignment(
    task?: Task
): WorkspaceUserAssignment {
    const maybeSelected: WorkspaceUserAssignmentState = task?.assignee
        ? {
              kind: "workspaceUser",
              workspaceUser: task.assignee,
          }
        : {
              kind: "unassigned",
          };
    const selected = writable<WorkspaceUserAssignmentState>(maybeSelected);
    const { subscribe } = derived<typeof selected, WorkspaceUser | undefined>(
        selected,
        ($selected, set) => {
            if ($selected.kind == "unassigned") {
                set(undefined);
            } else {
                const { workspaceUser } = $selected;
                set(workspaceUser);
            }
        }
    );
    const select = (selection: WorkspaceUserAssignmentInput) => {
        if (selection.kind === "unassigned") {
            selected.set(selection);
        } else {
            selected.set({
                kind: "workspaceUser",
                workspaceUser: selection.workspaceUser,
            });
        }
    };
    // No matter what, we always unassign
    const deselect = (_selection: WorkspaceUserAssignmentInput) => {
        selected.set({ kind: "unassigned" });
    };
    return {
        select,
        deselect,
        selected: readonly(selected),
        subscribe,
    };
}
