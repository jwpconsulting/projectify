import { _selectedWorkspaceUser } from "./selectedWorkspaceUser";
import type {
    WorkspaceUserSearch,
    WorkspaceUserSearchResults,
} from "./workspaceUser";

import { currentWorkspaceBoardSections } from "$lib/stores/dashboard/workspaceBoardSection";
import {
    selectWorkspaceUser,
    deselectWorkspaceUser,
    createWorkspaceUserSearchResults,
    currentWorkspaceUsers,
    createTasksPerUser,
    createWorkspaceUserSearch,
} from "$lib/stores/dashboard/workspaceUser";
import type { WorkspaceUserSearchStore } from "$lib/types/stores";

const workspaceUserSearch: WorkspaceUserSearch = createWorkspaceUserSearch();

const workspaceUserSearchResults: WorkspaceUserSearchResults =
    createWorkspaceUserSearchResults(
        currentWorkspaceUsers,
        workspaceUserSearch
    );

export const workspaceUserSearchModule: WorkspaceUserSearchStore = {
    select: selectWorkspaceUser,
    deselect: deselectWorkspaceUser,
    selected: _selectedWorkspaceUser,
    search: workspaceUserSearch,
    searchResults: workspaceUserSearchResults,
    tasksPerUser: createTasksPerUser(currentWorkspaceBoardSections),
};
