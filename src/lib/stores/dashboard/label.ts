import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import { searchAmong } from "$lib/stores/util";
import type { SearchInput } from "$lib/types/base";
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
