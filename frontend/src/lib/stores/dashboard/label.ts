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
import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import { searchAmong } from "$lib/stores/util";
import type { SearchInput } from "$lib/types/base";
import type { Label } from "$lib/types/workspace";
import { currentProject } from "./project";
import { currentWorkspace } from "./workspace";

type CurrentWorkspaceLabels = Readable<readonly Label[] | undefined>;
export const currentWorkspaceLabels: CurrentWorkspaceLabels = derived<
    [typeof currentWorkspace, typeof currentProject],
    readonly Label[] | undefined
>(
    [currentWorkspace, currentProject],
    ([$currentWorkspace, $currentProject], set) => {
        set(
            $currentWorkspace.value?.labels ??
                $currentProject.value?.workspace.labels,
        );
    },
    undefined,
);
// LabelFilter and Selection
function searchLabels(
    labels: readonly Label[],
    searchInput: SearchInput,
): readonly Label[] {
    if (searchInput === undefined) {
        return labels;
    }
    return searchAmong(["name"], labels, searchInput);
}

type LabelFilter = Readable<SearchInput>;
export function createLabelFilter(): LabelFilter {
    return writable<SearchInput>(undefined);
}

type LabelSearchResults = Readable<readonly Label[]>;

export function createLabelSearchResults(
    currentWorkspaceLabels: CurrentWorkspaceLabels,
    labelSearch: LabelFilter,
): LabelSearchResults {
    return derived<[CurrentWorkspaceLabels, LabelFilter], readonly Label[]>(
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
