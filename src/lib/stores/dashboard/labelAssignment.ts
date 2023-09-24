/*
 * Same design principle here as in ws users: We split label stores into
 * assignment (assigning a label to a task) and filter (filtering tasks by
 * labels)
 */

import { readonly, writable } from "svelte/store";

import { getAsync } from "../util";

import type { LabelAssignment } from "$lib/types/stores";
import type {
    LabelAssignmentInput,
    LabelAssignmentState,
} from "$lib/types/ui";
import type { Label, Task } from "$lib/types/workspace";

export function createLabelAssignment(
    task?: Task,
    // TODO maybe we can get rid of selectCallback this completely?
    selectCallback?: (labelUuid: string, selected: boolean) => void
): LabelAssignment {
    const maybeLabels: Label[] = task?.labels ?? [];
    const selection: LabelAssignmentState =
        maybeLabels.length > 0
            ? {
                  kind: "labels",
                  labelUuids: new Set(maybeLabels.map((l) => l.uuid)),
              }
            : { kind: "noLabel" };
    const selected = writable<LabelAssignmentState>(selection);
    const selectOrDeselectLabel = (
        select: boolean,
        labelAssignmentInput: LabelAssignmentInput
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
                } else {
                    return {
                        ...$selected,
                        labelUuids: $selected.labelUuids.add(labelUuid),
                    };
                }
            });
            if (selectCallback) {
                selectCallback(labelUuid, select);
            }
        }
    };
    return {
        select: (labelAssignmentInput: LabelAssignmentInput) => {
            selectOrDeselectLabel(true, labelAssignmentInput);
        },
        deselect: (labelAssignmentInput: LabelAssignmentInput) => {
            selectOrDeselectLabel(false, labelAssignmentInput);
        },
        // TODO current selection should come from current task labels
        selected: readonly(selected),
        async evaluate(): Promise<string[]> {
            const state = await getAsync(selected);
            if (state.kind === "noLabel") {
                return [];
            }
            return [...state.labelUuids];
        },
    };
}
