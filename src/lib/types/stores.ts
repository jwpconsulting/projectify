import type { Readable, Writable } from "svelte/store";

import type {
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
    TasksPerUser,
    LabelSelection,
    LabelSelectionInput,
} from "$lib/types/ui";
import type { WorkspaceUser, Label } from "$lib/types/workspace";

export type WorkspaceUserSearchModule = {
    select: (selection: WorkspaceUserSelectionInput) => void;
    deselect: (selection: WorkspaceUserSelectionInput) => void;
    // TODO make readonly (the two methods above are the only setters)
    selected: Writable<WorkspaceUserSelection>;
    tasksPerUser: Readable<TasksPerUser>;
    // TODO make readonly (should only be writable from inside store)
    search: Writable<string>;
    searchResults: Readable<WorkspaceUser[]>;
};

export type LabelSearchModule = {
    select: (selection: LabelSelectionInput) => void;
    deselect: (selection: LabelSelectionInput) => void;
    // TODO make readonly
    selected: Writable<LabelSelection>;
    // TODO make readonly
    search: Writable<string>;
    searchResults: Readable<Label[]>;
};
