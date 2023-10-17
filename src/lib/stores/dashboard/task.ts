import { derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";

import {
    getTask,
    deleteTask as repositoryDeleteTask,
} from "$lib/repository/workspace";
import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
import { currentWorkspaceBoard } from "$lib/stores/dashboard/workspaceBoard";
import { filterByWorkspaceUser } from "$lib/stores/dashboard/workspaceUserFilter";
import { searchAmong } from "$lib/stores/util";
import { createWsStore } from "$lib/stores/wsSubscription";
import type {
    Task,
    // XXX only use TaskWithWorkspace
    TaskWithWorkspaceBoardSection,
    TaskWithWorkspace,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

export const taskSearchInput = writable<string>("");

// Clear on workspace board change
// TODO clarify if this subscription still makes sense
// It's good to unsubscribe whenever we can
// Justus 2023-08-30
currentWorkspaceBoard.subscribe((_$currentWorkspaceBoard) => {
    selectedLabels.set({ kind: "allLabels" });
    filterByWorkspaceUser({ kind: "allWorkspaceUsers" });
    taskSearchInput.set("");
});

// TODO can we use undefined here instead?
type CurrentSearchedTasks = Readable<TaskWithWorkspaceBoardSection[] | null>;

export function createCurrentSearchedTasks(
    currentWorkspaceBoardSections: Readable<WorkspaceBoardSection[]>,
    taskSearchInput: Readable<string>
): CurrentSearchedTasks {
    return derived<
        [typeof currentWorkspaceBoardSections, typeof taskSearchInput],
        TaskWithWorkspaceBoardSection[] | null
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
): TaskWithWorkspaceBoardSection[] {
    const sectionTasks: TaskWithWorkspaceBoardSection[][] = sections.map(
        (workspace_board_section) =>
            (workspace_board_section.tasks ?? []).map((task: Task) => {
                return { ...task, workspace_board_section };
            })
    );
    const tasks = sectionTasks.flat();
    return searchAmong<TaskWithWorkspaceBoardSection>(
        ["title"],
        tasks,
        searchText
    );
}

export const currentTask = createWsStore<TaskWithWorkspace>("task", getTask);

export async function deleteTask(task: Task) {
    await repositoryDeleteTask(task);
}
