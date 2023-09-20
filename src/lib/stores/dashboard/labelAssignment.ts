/*
 * Same design principle here as in ws users: We split label stores into
 * assignment (assigning a label to a task) and filter (filtering tasks by
 * labels)
 */
import { writable } from "svelte/store";

import type { LabelAssignment } from "$lib/types/stores";
import type { LabelSelection, LabelSelectionInput } from "$lib/types/ui";
import type { Task } from "$lib/types/workspace";

export function createLabelSearchStore(
    task: Task | null,
    selectCallback: (labelUuid: string, selected: boolean) => void
): LabelAssignment {
    const labelSelected: LabelSelection =
        task?.labels && task.labels.length > 0
            ? {
                  kind: "labels",
                  labelUuids: new Set(task.labels.map((l) => l.uuid)),
              }
            : { kind: "noLabel" };
    const selectOrDeselectLabel = (
        select: boolean,
        labelSelectionInput: LabelSelectionInput
    ) => {
        const { kind } = labelSelectionInput;
        if (kind === "noLabel") {
            console.error("No API for removing all labels");
            throw new Error("TODO");
        } else if (kind === "allLabels") {
            // XXX Clearly, allLabels only makes sense for side nav, not when
            // assigning labels to tasks
            console.error("No API for assigning all labels");
            throw new Error("TODO");
        } else {
            const { labelUuid } = labelSelectionInput;
            selectCallback(labelUuid, select);
        }
    };
    return {
        select: (labelSelectionInput: LabelSelectionInput) => {
            selectOrDeselectLabel(true, labelSelectionInput);
        },
        deselect: (labelSelectionInput: LabelSelectionInput) => {
            selectOrDeselectLabel(false, labelSelectionInput);
        },
        selected: writable<LabelSelection>(labelSelected),
        async createLabel() {
            await new Promise(console.error);
            throw new Error("Not implemented");
        },
    };
}
