// XXX "stores.ts" should be renamed "modules.ts" maybe?
import type { Readable, Writable } from "svelte/store";

import type { RepositoryContext } from "./repository";

import type {
    LabelSelectionInput,
    WorkspaceUserSelection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type {
    CreateTask,
    NewTask,
    Task,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

export interface WorkspaceUserFilter {
    select: (selection: WorkspaceUserSelectionInput) => unknown;
    deselect: (selection: WorkspaceUserSelectionInput) => unknown;
    selected: Readable<WorkspaceUserSelection>;
}

export interface WorkspaceUserAssignment {
    select: (selection: WorkspaceUserSelectionInput) => unknown;
    deselect: (selection: WorkspaceUserSelectionInput) => unknown;
    selected: Readable<WorkspaceUserSelection>;
}

export interface LabelFilter {
    select: (selection: LabelSelectionInput) => unknown;
    deselect: (selection: LabelSelectionInput) => unknown;
}

export interface LabelAssignment {
    select: (selection: LabelSelectionInput) => unknown;
    deselect: (selection: LabelSelectionInput) => unknown;
}

// It would make sense to rename all Module to Store

// XXX
// This is a mess!
// this contains whatever is shared between creating / updating tasks
export interface CreateOrUpdateTaskModule {
    canCreateOrUpdate: Readable<boolean>;
    createOrUpdateTask: () => unknown;
    workspaceUserFilter: WorkspaceUserFilter;
    labelSearchModule: LabelFilter;
}

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

// Functions needed to move task around inside section or between sections
export interface MoveTaskModule {
    moveToBottom?: () => Promise<void>;
    moveToTop?: () => Promise<void>;
    moveToWorkspaceBoardSection: (
        workspaceBoardSection: WorkspaceBoardSection
    ) => Promise<void>;
}

const subscriptionTypes = ["workspace", "workspace-board", "task"] as const;
export type SubscriptionType = (typeof subscriptionTypes)[number];

export interface WsResource<T> extends Readable<T> {
    loadUuid: (
        uuid: string,
        repositoryContext?: RepositoryContext
    ) => Promise<T>;
}
