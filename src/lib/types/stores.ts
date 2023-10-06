// XXX "stores.ts" should be renamed "modules.ts" maybe?
import type { Readable, Subscriber, Writable } from "svelte/store";

import type { RepositoryContext } from "./repository";

import type {
    LabelAssignmentInput,
    WorkspaceUserAssignmentInput,
    LabelAssignmentState,
    WorkspaceUserAssignmentState,
} from "$lib/types/ui";
import type { Label, SubTask, WorkspaceUser } from "$lib/types/workspace";

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
    // TODO Might even completely remove this:
    selected: Readable<LabelAssignmentState>;
}

export interface SubTaskAssignment extends Writable<Partial<SubTask>[]> {
    addSubTask: () => void;
}

const subscriptionTypes = ["workspace", "workspace-board", "task"] as const;
export type SubscriptionType = (typeof subscriptionTypes)[number];

// A subscriber that can deal with possible undefined values
export type MaybeSubscriber<T> = Subscriber<T | undefined>;
export interface WsResource<T> extends Readable<T | undefined> {
    loadUuid: (
        uuid: string,
        repositoryContext?: RepositoryContext
    ) => Promise<T>;
    unwrap: () => T;
}
