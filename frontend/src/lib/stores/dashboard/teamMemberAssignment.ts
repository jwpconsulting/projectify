// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { derived, readonly, writable } from "svelte/store";

import type { TeamMemberAssignment } from "$lib/types/stores";
import type {
    TeamMemberAssignmentInput,
    TeamMemberAssignmentState,
} from "$lib/types/ui";
import type {
    ProjectDetailTask,
    TaskDetail,
    ProjectDetailAssignee,
} from "$lib/types/workspace";

export function createTeamMemberAssignment(
    task?: TaskDetail | ProjectDetailTask,
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
    const { subscribe } = derived<
        typeof selected,
        ProjectDetailAssignee | null
    >(selected, ($selected, set) => {
        if ($selected.kind == "unassigned") {
            set(null);
        } else {
            const { teamMember } = $selected;
            set(teamMember);
        }
    });
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
