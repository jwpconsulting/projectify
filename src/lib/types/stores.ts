// XXX "stores.ts" should be renamed "modules.ts" maybe?
import type { Readable } from "svelte/store";

import type { RepositoryContext } from "./repository";

import type {
    LabelAssignmentInput,
    WorkspaceUserAssignmentInput,
    LabelAssignmentState,
    WorkspaceUserAssignmentState,
} from "$lib/types/ui";
import type {
    Label,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";

export interface WorkspaceUserAssignment
    extends Readable<WorkspaceUser | undefined> {
    select: (selection: WorkspaceUserAssignmentInput) => unknown;
    deselect: (selection: WorkspaceUserAssignmentInput) => unknown;
    // Might even completely remove this:
    selected: Readable<WorkspaceUserAssignmentState>;
}

export interface LabelAssignment extends Readable<Label[]> {
    select: (selection: LabelAssignmentInput) => unknown;
    deselect: (selection: LabelAssignmentInput) => unknown;
    // Might even completely remove this:
    selected: Readable<LabelAssignmentState>;
    // Might even completely remove this:
    evaluate: () => Promise<string[]>;
}

// It would make sense to rename all Module to Store

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
