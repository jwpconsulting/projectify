import { _selectedWorkspaceUser } from "./selectedWorkspaceUser";
import type {
    WorkspaceUserSearch,
    WorkspaceUserSearchResults,
} from "./workspaceUser";

import { currentWorkspaceBoardSections } from "$lib/stores/dashboard/workspaceBoardSection";
import {
    createWorkspaceUserSearchResults,
    currentWorkspaceUsers,
    createTasksPerUser,
    createWorkspaceUserFilter,
} from "$lib/stores/dashboard/workspaceUser";
import type { WorkspaceUserFilter } from "$lib/types/stores";
import type {
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";

const workspaceUserSearch: WorkspaceUserSearch = createWorkspaceUserFilter();

export function filterByWorkspaceUser(selection: WorkspaceUserSelectionInput) {
    _selectedWorkspaceUser.update(
        ($selectedWorkspaceUser: WorkspaceUserSelection) => {
            if (selection.kind === "allWorkspaceUsers") {
                return { kind: "allWorkspaceUsers" };
            } else if (selection.kind === "unassigned") {
                if ($selectedWorkspaceUser.kind === "unassigned") {
                    return { kind: "allWorkspaceUsers" };
                } else {
                    return { kind: "unassigned" };
                }
            } else {
                const selectionUuid = selection.workspaceUser.uuid;
                if ($selectedWorkspaceUser.kind === "workspaceUsers") {
                    $selectedWorkspaceUser.workspaceUserUuids.add(
                        selectionUuid
                    );
                    return $selectedWorkspaceUser;
                } else {
                    const workspaceUserUuids = new Set<string>();
                    workspaceUserUuids.add(selectionUuid);
                    return { kind: "workspaceUsers", workspaceUserUuids };
                }
            }
        }
    );
}

export function unfilterByWorkspaceUser(
    selection: WorkspaceUserSelectionInput
) {
    _selectedWorkspaceUser.update(
        ($selectedWorkspaceUser: WorkspaceUserSelection) => {
            if (selection.kind === "allWorkspaceUsers") {
                return { kind: "allWorkspaceUsers" };
            } else if (selection.kind === "unassigned") {
                if ($selectedWorkspaceUser.kind === "unassigned") {
                    return { kind: "allWorkspaceUsers" };
                } else {
                    return { kind: "unassigned" };
                }
            } else {
                const selectionUuid = selection.workspaceUser.uuid;
                if ($selectedWorkspaceUser.kind === "workspaceUsers") {
                    $selectedWorkspaceUser.workspaceUserUuids.delete(
                        selectionUuid
                    );
                    if ($selectedWorkspaceUser.workspaceUserUuids.size === 0) {
                        return { kind: "allWorkspaceUsers" };
                    } else {
                        return $selectedWorkspaceUser;
                    }
                } else {
                    return { kind: "allWorkspaceUsers" };
                }
            }
        }
    );
}

const workspaceUserSearchResults: WorkspaceUserSearchResults =
    createWorkspaceUserSearchResults(
        currentWorkspaceUsers,
        workspaceUserSearch
    );

export const workspaceUserFilter: WorkspaceUserFilter = {
    select: filterByWorkspaceUser,
    deselect: unfilterByWorkspaceUser,
    selected: _selectedWorkspaceUser,
    search: workspaceUserSearch,
    searchResults: workspaceUserSearchResults,
    tasksPerUser: createTasksPerUser(currentWorkspaceBoardSections),
};
