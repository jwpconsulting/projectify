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
// XXX "stores.ts" should be renamed "modules.ts" maybe?
import type { Readable, Subscriber, Writable } from "svelte/store";

import type {
    LabelAssignmentInput,
    WorkspaceUserAssignmentInput,
    LabelAssignmentState,
    WorkspaceUserAssignmentState,
} from "$lib/types/ui";
import type {
    CreateUpdateSubTask,
    Label,
    WorkspaceUser,
} from "$lib/types/workspace";

import type { RepositoryContext } from "./repository";

export interface WorkspaceUserAssignment
    extends Readable<WorkspaceUser | undefined> {
    select: (selection: WorkspaceUserAssignmentInput) => unknown;
    deselect: (selection: WorkspaceUserAssignmentInput) => unknown;
    // Might even completely remove this:
    selected: Readable<WorkspaceUserAssignmentState>;
}

export interface LabelAssignment extends Readable<Label[] | undefined> {
    select: (selection: LabelAssignmentInput) => unknown;
    deselect: (selection: LabelAssignmentInput) => unknown;
    // TODO Might even completely remove this:
    selected: Readable<LabelAssignmentState>;
}

export interface SubTaskAssignment
    extends Writable<Partial<CreateUpdateSubTask>[]> {
    addSubTask: () => void;
    removeSubTask: (where: number) => void;
    // if all sub tasks are non-partial, an inner store will return the whole
    // list of sub tasks.
    subTasks: Readable<CreateUpdateSubTask[] | undefined>;
    moveSubTaskUp: (where: number) => void;
    moveSubTaskDown: (where: number) => void;
}

const subscriptionTypes = ["workspace", "workspace-board", "task"] as const;
export type SubscriptionType = (typeof subscriptionTypes)[number];

// A subscriber that can deal with possible undefined values
export type MaybeSubscriber<T> = Subscriber<T | undefined>;

export type RepoGetter<T> = (
    uuid: string,
    repositoryContext: RepositoryContext,
) => Promise<T | undefined>;
export interface WsResource<T> extends Readable<T | undefined> {
    loadUuid: RepoGetter<T>;
    unwrap: () => T;
}
