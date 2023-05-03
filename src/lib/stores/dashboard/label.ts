import Fuse from "fuse.js";
import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";
import { fuseSearchThreshold } from "$lib/config";

import type { Label } from "$lib/types/workspace";
import type { LabelSelection, LabelSelectionInput } from "$lib/types/ui";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";

type CurrentWorkspaceLabels = Readable<Label[]>;
export const currentWorkspaceLabels: CurrentWorkspaceLabels = derived<
    [typeof currentWorkspace],
    Label[]
>(
    [currentWorkspace],
    ([$currentWorkspace], set) => {
        if (!$currentWorkspace) {
            set([]);
            return;
        }
        if (!$currentWorkspace.labels) {
            throw new Error("Expected $currentWorkspace.labels");
        }
        set($currentWorkspace.labels);
    },
    []
);
// LabelSearch and Selection
function searchLabels(labels: Label[], searchInput: string): Label[] {
    if (searchInput === "") {
        return labels;
    }
    const searchEngine = new Fuse(labels, {
        keys: ["name"],
        threshold: fuseSearchThreshold,
        shouldSort: false,
    });
    const result = searchEngine.search(searchInput);
    return result.map((res: Fuse.FuseResult<Label>) => res.item);
}

type LabelSearch = Readable<string>;
export const labelSearch = writable<string>("");

type LabelSearchResults = Readable<Label[]>;

export function createLabelSearchResults(
    currentWorkspaceLabels: CurrentWorkspaceLabels,
    labelSearch: LabelSearch
): LabelSearchResults {
    return derived<[CurrentWorkspaceLabels, LabelSearch], Label[]>(
        [currentWorkspaceLabels, labelSearch],
        ([currentWorkspaceLabels, labelSearch], set) => {
            set(searchLabels(currentWorkspaceLabels, labelSearch));
        },
        []
    );
}

export const selectedLabels = writable<LabelSelection>({ kind: "allLabels" });

export function selectLabel(selection: LabelSelectionInput) {
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
export function deselectLabel(selection: LabelSelectionInput) {
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
