import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import { createLabel as repositoryCreateLabel } from "$lib/repository/workspace";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import { searchAmong } from "$lib/stores/util";
import type { SearchInput } from "$lib/types/base";
import type { LabelSearchStore } from "$lib/types/stores";
import type { LabelSelection, LabelSelectionInput } from "$lib/types/ui";
import type { Label, Workspace } from "$lib/types/workspace";

type CurrentWorkspaceLabels = Readable<Label[]>;
export const currentWorkspaceLabels: CurrentWorkspaceLabels = derived<
    typeof currentWorkspace,
    Label[]
    // Derived stores are initialized with undefined
>(
    currentWorkspace,
    ($currentWorkspace: Workspace | undefined, set) => {
        if (!$currentWorkspace) {
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
function searchLabels(labels: Label[], searchInput: SearchInput): Label[] {
    if (searchInput === undefined) {
        return labels;
    }
    return searchAmong(["name"], labels, searchInput);
}

type LabelSearch = Readable<SearchInput>;
export const createLabelSearch = () => writable<string>(undefined);

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

// XXX
// Again, we need to make this using a factory thing somewhere
// Otherwise we duplicate code in 3 different locations (task creation,
// side nav, task updating)
// Justus 2023-05-02
const labelSearch = createLabelSearch();
export const labelSearchModule: LabelSearchStore = {
    select: selectLabel,
    deselect: deselectLabel,
    selected: selectedLabels,
    search: labelSearch,
    searchResults: createLabelSearchResults(
        currentWorkspaceLabels,
        labelSearch
    ),
    async createLabel(color: number, name: string) {
        // XXX hackish
        const $currentWorkspace = await new Promise<Workspace>((resolve) => {
            const unsubscribe = currentWorkspace.subscribe(resolve);
            unsubscribe();
        });
        await repositoryCreateLabel($currentWorkspace, name, color);
    },
};
