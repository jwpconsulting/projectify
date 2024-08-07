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
import type { Readable, Writable } from "svelte/store";

import type {
    LabelAssignmentInput,
    TeamMemberAssignmentInput,
    LabelAssignmentState,
    TeamMemberAssignmentState,
} from "$lib/types/ui";
import type {
    CreateUpdateSubTask,
    Label,
    ProjectDetailAssignee,
} from "$lib/types/workspace";

export interface TeamMemberAssignment
    extends Readable<ProjectDetailAssignee | null> {
    select: (selection: TeamMemberAssignmentInput) => unknown;
    deselect: (selection: TeamMemberAssignmentInput) => unknown;
    // Might even completely remove this:
    selected: Readable<TeamMemberAssignmentState>;
}

export interface LabelAssignment extends Readable<Label[]> {
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
    subTasks: Readable<CreateUpdateSubTask[]>;
    moveSubTaskUp: (where: number) => void;
    moveSubTaskDown: (where: number) => void;
}

// TODO make a simple union type
const subscriptionTypes = ["workspace", "project", "task"] as const;
export type SubscriptionType = (typeof subscriptionTypes)[number];

export interface HasUuid {
    uuid: string;
}
export type RepoGetter<T extends HasUuid> = (
    uuid: string,
) => Promise<T | undefined>;
export interface WsResourceContainer<T extends HasUuid> {
    value: T | undefined;
    orPromise: (t: Promise<T>) => Promise<T>;
    or: (t: T) => T;
}
export interface WsResource<T extends HasUuid>
    extends Readable<WsResourceContainer<T>> {
    loadUuid: RepoGetter<T>;
}
