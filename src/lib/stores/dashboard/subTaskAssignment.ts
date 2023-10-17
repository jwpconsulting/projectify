import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import type { SubTaskAssignment } from "$lib/types/stores";
import type { CreateUpdateSubTask, Task } from "$lib/types/workspace";

function filterSubTasks(
    subTasks: Partial<CreateUpdateSubTask>[]
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
        el ? [el] : []
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
        undefined
    );
    return {
        subscribe,
        set,
        update,
        addSubTask,
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
