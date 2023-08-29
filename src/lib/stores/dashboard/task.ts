import lodash from "lodash";
import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import {
    getTask,
    deleteTask as repositoryDeleteTask,
} from "$lib/repository/workspace";
import { selectedLabels } from "$lib/stores/dashboard/label";
import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard/workspaceBoard";
import { selectWorkspaceUser } from "$lib/stores/dashboard/workspaceUser";
import { createWsStore, searchAmong } from "$lib/stores/util";
import type { Task, WorkspaceBoardSection } from "$lib/types/workspace"; // XXX Remove this

export const taskSearchInput = writable<string>("");
export const currentTaskUuid = writable<string | null>(null);

// Clear on workspace board change
currentWorkspaceBoardUuid.subscribe((_uuid) => {
    selectedLabels.set({ kind: "allLabels" });
    selectWorkspaceUser({ kind: "allWorkspaceUsers" });
    taskSearchInput.set("");
});

type CurrentSearchedTasks = Readable<Task[] | null>;

export function createCurrentSearchedTasks(
    currentWorkspaceBoardSections: Readable<WorkspaceBoardSection[]>,
    taskSearchInput: Readable<string>
): CurrentSearchedTasks {
    return derived<
        [typeof currentWorkspaceBoardSections, typeof taskSearchInput],
        Task[] | null
    >(
        [currentWorkspaceBoardSections, taskSearchInput],
        ([$currentWorkspaceBoardSections, $taskSearchInput], set) => {
            if ($taskSearchInput == "") {
                set(null);
            } else {
                set(
                    searchTasks(
                        $currentWorkspaceBoardSections,
                        $taskSearchInput
                    )
                );
            }
        },
        null
    );
}

function searchTasks(
    sections: WorkspaceBoardSection[],
    searchText: string
): Task[] {
    const tasks: Task[] = lodash.flatten(
        sections.map((section) => (section.tasks ? section.tasks : []))
    );

    return searchAmong<Task>(["title"], tasks, searchText);
}

export const currentTask = createWsStore<Task>(
    "task",
    currentTaskUuid,
    getTask
);

export async function deleteTask(task: Task) {
    await repositoryDeleteTask(task);
}
