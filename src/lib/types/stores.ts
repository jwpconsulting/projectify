// XXX "stores.ts" should be renamed "modules.ts" maybe?
import type { Readable, Writable } from "svelte/store";

import type { RepositoryContext } from "./repository";

import type {
    LabelAssignmentInput,
    WorkspaceUserSelection,
    WorkspaceUserAssignmentInput,
    LabelAssignmentState,
} from "$lib/types/ui";
import type {
    CreateTask,
    NewTask,
    Task,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

export interface WorkspaceUserAssignment {
    select: (selection: WorkspaceUserAssignmentInput) => unknown;
    deselect: (selection: WorkspaceUserAssignmentInput) => unknown;
    selected: Readable<WorkspaceUserSelection>;
}

export interface LabelAssignment {
    select: (selection: LabelAssignmentInput) => unknown;
    deselect: (selection: LabelAssignmentInput) => unknown;
    selected: Readable<LabelAssignmentState>;
    evaluate: () => Promise<string[]>;
}

// It would make sense to rename all Module to Store

// XXX
// This is a mess!
// this contains whatever is shared between creating / updating tasks
export interface CreateOrUpdateTaskModule {
    workspaceUserAssignment: WorkspaceUserAssignment;
    labelAssignment: LabelAssignment;
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
