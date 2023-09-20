/*
 * Same design principle here as in ws users: We split label stores into
 * assignment (assigning a label to a task) and filter (filtering tasks by
 * labels)
 */

import { readable } from "svelte/store";

import type { LabelAssignment } from "$lib/types/stores";
import type { LabelAssignmentInput } from "$lib/types/ui";
import type { Task } from "$lib/types/workspace";

export function createLabelAssignment(
    task: Task | null,
    selectCallback: (labelUuid: string, selected: boolean) => void
): LabelAssignment {
    const selectOrDeselectLabel = (
        select: boolean,
        labelAssignmentInput: LabelAssignmentInput
    ) => {
        const { kind } = labelAssignmentInput;
        if (kind === "noLabel") {
            console.error("No API for removing all labels");
            throw new Error("TODO");
        } else {
            const { labelUuid } = labelAssignmentInput;
            selectCallback(labelUuid, select);
        }
    };
    return {
        select: (labelAssignmentInput: LabelAssignmentInput) => {
            selectOrDeselectLabel(true, labelAssignmentInput);
        },
        deselect: (labelAssignmentInput: LabelAssignmentInput) => {
            selectOrDeselectLabel(false, labelAssignmentInput);
        },
        // TODO
        selected: readable({ kind: "noLabel" }),
    };
}
