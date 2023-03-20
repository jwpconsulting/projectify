import type { Readable, Writable } from "svelte/store";

import type {
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
    TasksPerUser,
} from "$lib/types/ui";
import type { WorkspaceUser } from "$lib/types/workspace";

export type WorkspaceUserSearchModule = {
    select: (selection: WorkspaceUserSelectionInput) => void;
    deselect: (selection: WorkspaceUserSelectionInput) => void;
    selected: Writable<WorkspaceUserSelection>;
    tasksPerUser: Readable<TasksPerUser>;
    search: Writable<string>;
    searchResults: Readable<WorkspaceUser[]>;
};
