import { writable } from "svelte/store";

import type { SubTaskAssignment } from "$lib/types/stores";
import type { SubTask, Task } from "$lib/types/workspace";

export function createSubTaskAssignment(task: Task): SubTaskAssignment {
    const sub_tasks = task.sub_tasks ?? [];
    const { subscribe } = writable<Partial<SubTask>[]>(sub_tasks);
    return {
        subscribe,
    };
}
