// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { derived, readonly, writable } from "svelte/store";

import type { WorkspaceUserAssignment } from "$lib/types/stores";
import type {
    WorkspaceUserAssignmentInput,
    WorkspaceUserAssignmentState,
} from "$lib/types/ui";
import type { Task, WorkspaceUser } from "$lib/types/workspace";

export function createWorkspaceUserAssignment(
    task?: Task,
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
        },
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
