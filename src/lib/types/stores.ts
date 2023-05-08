// XXX "stores.ts" should be renamed "modules.ts" maybe?
import type { Readable, Writable } from "svelte/store";

import type {
    LabelSelection,
    LabelSelectionInput,
    TasksPerUser,
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type {
    CreateTask,
    CreateWorkspaceBoardSection,
    Label,
    NewTask,
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceUser,
} from "$lib/types/workspace";

// It would make sense to rename all Module to Store

export type WorkspaceSearchModule = {
    // TODO for a consistent API we would have workspaces as searchResults here
    workspaces: Readable<Workspace[] | null>;
    currentWorkspace: Readable<Workspace | null>;
    setWorkspaces: () => Promise<void>;
};

// XXX I took the liberty of adding workspace board creation into here
// Not sure if that is good Justus 2023-05-01
export type WorkspaceBoardSearchModule = {
    // TODO for a consistent API we would have workspace boards as
    // searchResults here
    currentWorkspaceBoardUuid: Readable<string | null>;
    currentWorkspaceBoard: Readable<WorkspaceBoard | null>;
    currentWorkspace: Readable<Workspace | null>;
};

export type WorkspaceUserSearchModule = {
    select: (selection: WorkspaceUserSelectionInput) => void;
    deselect: (selection: WorkspaceUserSelectionInput) => void;
    selected: Readable<WorkspaceUserSelection>;
    tasksPerUser: Readable<TasksPerUser>;
    search: Writable<string>;
    searchResults: Readable<WorkspaceUser[]>;
};

export type LabelSearchModule = {
    select: (selection: LabelSelectionInput) => void;
    deselect: (selection: LabelSelectionInput) => void;
    selected: Readable<LabelSelection>;
    // TODO make readonly
    search: Writable<string>;
    searchResults: Readable<Label[]>;
    createLabel: (color: number, name: string) => Promise<void>;
};

export type SideNavModule = {
    sideNavOpen: Readable<boolean>;
    toggleSideNavOpen: () => void;
    showWorkspaceContextMenu: (anchor: HTMLElement) => void;
    showSideNavContextMenu: (anchor: HTMLElement) => void;
};

export type WorkspaceBoardSectionModule = {
    workspaceBoardSectionClosed: Writable<Set<string>>;
    toggleWorkspaceBoardSectionOpen: (
        workspaceBoardSectionUuid: string
    ) => void;
};

export type NewWorkspaceBoardSectionModule = {
    createWorkspaceBoardSection: (
        workspaceBoard: WorkspaceBoard,
        workspaceBoardSection: CreateWorkspaceBoardSection
    ) => void;
};

// XXX
// This is a mess!
// this contains whatever is shared between creating / updating tasks
export type CreateOrUpdateTaskModule = {
    canCreateOrUpdate: Readable<boolean>;
    createOrUpdateTask: () => void;
    workspaceUserSearchModule: WorkspaceUserSearchModule;
    labelSearchModule: LabelSearchModule;
};

export type TaskModule = {
    task: Task;
    updateTask: Writable<Partial<Task>>;
    showUpdateWorkspaceUser: (anchor: HTMLElement) => void;
    showUpdateLabel: (anchor: HTMLElement) => void;
} & CreateOrUpdateTaskModule;

export type CreateTaskModule = {
    newTask: NewTask;
    createTask: Writable<Partial<CreateTask>>;
} & CreateOrUpdateTaskModule;
