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
/*
 * Same design principle here as in ws users: We split label stores into
 * assignment (assigning a label to a task) and filter (filtering tasks by
 * labels)
 */

import { derived, readonly, writable } from "svelte/store";

import type { LabelAssignment } from "$lib/types/stores";
import type {
    LabelAssignmentInput,
    LabelAssignmentState,
} from "$lib/types/ui";
import type { Label, Task } from "$lib/types/workspace";

import { currentWorkspaceLabels } from "./label";

function evaluateLabelAssignment(state: LabelAssignmentState): string[] {
    if (state.kind === "noLabel") {
        return [];
    }
    return [...state.labelUuids];
}

export function createLabelAssignment(task?: Task): LabelAssignment {
    const maybeLabels: Label[] = task?.labels ?? [];
    const selection: LabelAssignmentState =
        maybeLabels.length > 0
            ? {
                  kind: "labels",
                  labelUuids: new Set(maybeLabels.map((l) => l.uuid)),
              }
            : { kind: "noLabel" };
    const selected = writable<LabelAssignmentState>(selection);
    const { subscribe } = derived<
        [typeof selected, typeof currentWorkspaceLabels],
        Label[] | undefined
    >(
        [selected, currentWorkspaceLabels],
        ([$selected, $currentWorkspaceLabels], set) => {
            if ($currentWorkspaceLabels === undefined) {
                // This should not be hit
                return;
            }
            const labelUuids = evaluateLabelAssignment($selected);
            const labels = $currentWorkspaceLabels.filter((label) =>
                labelUuids.includes(label.uuid),
            );
            set(labels);
        },
        undefined,
    );
    const selectOrDeselectLabel = (
        select: boolean,
        labelAssignmentInput: LabelAssignmentInput,
    ) => {
        const { kind } = labelAssignmentInput;
        if (kind === "noLabel") {
            selected.set({ kind: "noLabel" });
        } else {
            const { labelUuid } = labelAssignmentInput;
            selected.update(($selected) => {
                if ($selected.kind === "noLabel") {
                    return {
                        kind: "labels",
                        labelUuids: new Set([labelUuid]),
                    };
                }
                const { labelUuids } = $selected;
                if (select) {
                    labelUuids.add(labelUuid);
                    return { ...$selected };
                }
                labelUuids.delete(labelUuid);
                if (labelUuids.size == 0) {
                    return { kind: "noLabel" };
                }
                return { ...$selected, labelUuids };
            });
        }
    };
    return {
        select: (labelAssignmentInput: LabelAssignmentInput) => {
            selectOrDeselectLabel(true, labelAssignmentInput);
        },
        deselect: (labelAssignmentInput: LabelAssignmentInput) => {
            selectOrDeselectLabel(false, labelAssignmentInput);
        },
        selected: readonly(selected),
        subscribe,
    };
}
