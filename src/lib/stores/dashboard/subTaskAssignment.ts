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
import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import type { SubTaskAssignment } from "$lib/types/stores";
import type { CreateUpdateSubTask, Task } from "$lib/types/workspace";

function filterSubTasks(
    subTasks: Partial<CreateUpdateSubTask>[],
): CreateUpdateSubTask[] | undefined {
    const nonPartials = subTasks.map((el: Partial<CreateUpdateSubTask>) => {
        if (el.done !== undefined && el.title !== undefined) {
            return {
                title: el.title,
                description: el.description,
                done: el.done,
                uuid: el.uuid,
            };
        }
        return undefined;
    });
    const filtered: CreateUpdateSubTask[] = nonPartials.flatMap((el) =>
        el ? [el] : [],
    );
    if (nonPartials.length !== filtered.length) {
        return;
    }
    return filtered;
}

export function createSubTaskAssignment(task?: Task): SubTaskAssignment {
    const existingSubTasks = task?.sub_tasks ?? [];
    const { subscribe, set, update } =
        writable<Partial<CreateUpdateSubTask>[]>(existingSubTasks);
    const addSubTask = () => {
        update(($subTasks) => {
            return [...$subTasks, { done: false }];
        });
    };
    const removeSubTask = (where: number) => {
        update(($subTasks) => {
            return $subTasks.filter((_s, ix) => ix !== where);
        });
    };
    const subTasks = derived<
        Readable<Partial<CreateUpdateSubTask>[]>,
        CreateUpdateSubTask[]
    >(
        { subscribe },
        ($subTaskAssignment, set) => {
            const filtered = filterSubTasks($subTaskAssignment);
            if (!filtered) {
                return;
            }
            set(filtered);
        },
        undefined,
    );
    return {
        subscribe,
        set,
        update,
        addSubTask,
        removeSubTask,
        subTasks,
        // [head?, before, where, tail?] ->
        // [head?, where, before, tail?]
        // where has to be > 1
        moveSubTaskUp(where: number) {
            update(($subTasks) => {
                if (where < 1 || where >= $subTasks.length) {
                    throw new Error("Trying to move sub task out of bounds");
                }
                return [
                    ...$subTasks.slice(0, where - 1),
                    ...$subTasks.slice(where, where + 1),
                    ...$subTasks.slice(where - 1, where),
                    ...$subTasks.slice(where + 1, undefined),
                ];
            });
        },
        // [head?, where, after, tail?] ->
        // [head?, after, where, tail?]
        // where has to be less than subTasks.length -1
        moveSubTaskDown(where: number) {
            update(($subTasks) => {
                if (where < 0 || where > $subTasks.length - 2) {
                    throw new Error("Trying to move sub task out of bounds");
                }
                return [
                    ...$subTasks.slice(0, where),
                    ...$subTasks.slice(where + 1, where + 2),
                    ...$subTasks.slice(where, where + 1),
                    ...$subTasks.slice(where + 2, undefined),
                ];
            });
        },
    };
}
