import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import { searchAmong } from "$lib/stores/util";
import type { SearchInput } from "$lib/types/base";
import type { Label, Workspace } from "$lib/types/workspace";

type CurrentWorkspaceLabels = Readable<Label[] | undefined>;
export const currentWorkspaceLabels: CurrentWorkspaceLabels = derived<
    typeof currentWorkspace,
    Label[] | undefined
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
    undefined,
);
// LabelFilter and Selection
function searchLabels(labels: Label[], searchInput: SearchInput): Label[] {
    if (searchInput === undefined) {
        return labels;
    }
    return searchAmong(["name"], labels, searchInput);
}

type LabelFilter = Readable<SearchInput>;
export function createLabelFilter(): LabelFilter {
    return writable<SearchInput>(undefined);
}

type LabelSearchResults = Readable<Label[]>;

export function createLabelSearchResults(
    currentWorkspaceLabels: CurrentWorkspaceLabels,
    labelSearch: LabelFilter,
): LabelSearchResults {
    return derived<[CurrentWorkspaceLabels, LabelFilter], Label[]>(
        [currentWorkspaceLabels, labelSearch],
        ([$currentWorkspaceLabels, $labelSearch], set) => {
            if ($currentWorkspaceLabels === undefined) {
                return;
            }
            set(searchLabels($currentWorkspaceLabels, $labelSearch));
        },
        [],
    );
}
