import { writable } from "svelte/store";

import {
    createLabelFilter,
    createLabelSearchResults,
    currentWorkspaceLabels,
} from "./label";
import { currentWorkspace } from "./workspace";

import { createLabel as repositoryCreateLabel } from "$lib/repository/workspace";
import type { LabelFilter } from "$lib/types/stores";
import type { LabelSelection, LabelSelectionInput } from "$lib/types/ui";
import type { Workspace } from "$lib/types/workspace";

/*
 * Here come the shared methods for filtering all tasks by one or more labels
 */
export const selectedLabels = writable<LabelSelection>({ kind: "allLabels" });

export function filterByLabel(selection: LabelSelectionInput) {
    selectedLabels.update((selectedLabels) => {
        if (selection.kind == "label") {
            if (selectedLabels.kind === "labels") {
                selectedLabels.labelUuids.add(selection.labelUuid);
                return selectedLabels;
            } else {
                return {
                    kind: "labels",
                    labelUuids: new Set([selection.labelUuid]),
                };
            }
        } else if (selection.kind == "noLabel") {
            return { kind: "noLabel" };
        } else {
            return { kind: "allLabels" };
        }
    });
}
export function unfilterByLabel(selection: LabelSelectionInput) {
    selectedLabels.update((selectedLabels) => {
        if (selection.kind == "label") {
            if (selectedLabels.kind === "labels") {
                selectedLabels.labelUuids.delete(selection.labelUuid);
                if (selectedLabels.labelUuids.size === 0) {
                    return { kind: "allLabels" };
                }
                return selectedLabels;
            } else {
                return selectedLabels;
            }
        } else if (selection.kind == "noLabel") {
            return { kind: "allLabels" };
        } else {
            return { kind: "noLabel" };
        }
    });
}
const labelSearch = createLabelFilter();
// All the variables in this module should have labelFilter themed names
export const labelFilterSearchResults = createLabelSearchResults(
    currentWorkspaceLabels,
    labelSearch
);
export const labelSearchModule: LabelFilter = {
    select: filterByLabel,
    deselect: unfilterByLabel,
    selected: selectedLabels,
    search: labelSearch,
    searchResults: labelFilterSearchResults,
    async createLabel(color: number, name: string) {
        // XXX hackish
        const $currentWorkspace = await new Promise<Workspace>((resolve) => {
            const unsubscribe = currentWorkspace.subscribe(resolve);
            unsubscribe();
        });
        await repositoryCreateLabel($currentWorkspace, name, color);
    },
};
