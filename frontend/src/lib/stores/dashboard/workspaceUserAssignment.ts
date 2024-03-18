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

import type { TeamMemberAssignment } from "$lib/types/stores";
import type {
    TeamMemberAssignmentInput,
    TeamMemberAssignmentState,
} from "$lib/types/ui";
import type { Task, TeamMember } from "$lib/types/workspace";

export function createTeamMemberAssignment(
    task?: Task,
): TeamMemberAssignment {
    const maybeSelected: TeamMemberAssignmentState = task?.assignee
        ? {
              kind: "teamMember",
              teamMember: task.assignee,
          }
        : {
              kind: "unassigned",
          };
    const selected = writable<TeamMemberAssignmentState>(maybeSelected);
    const { subscribe } = derived<typeof selected, TeamMember | undefined>(
        selected,
        ($selected, set) => {
            if ($selected.kind == "unassigned") {
                set(undefined);
            } else {
                const { teamMember } = $selected;
                set(teamMember);
            }
        },
    );
    const select = (selection: TeamMemberAssignmentInput) => {
        if (selection.kind === "unassigned") {
            selected.set(selection);
        } else {
            selected.set({
                kind: "teamMember",
                teamMember: selection.teamMember,
            });
        }
    };
    // No matter what, we always unassign
    const deselect = (_selection: TeamMemberAssignmentInput) => {
        selected.set({ kind: "unassigned" });
    };
    return {
        select,
        deselect,
        selected: readonly(selected),
        subscribe,
    };
}
