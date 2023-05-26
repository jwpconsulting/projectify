import Fuse from "fuse.js";
import lodash from "lodash";
import { get, derived, writable } from "svelte/store";
import type { Readable } from "svelte/store";
import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard/workspaceBoard";
import { selectWorkspaceUser } from "$lib/stores/dashboard/workspaceUser";

import { selectedLabels } from "$lib/stores/dashboard/label";
import { fuseSearchThreshold } from "$lib/config";
import { getTask } from "$lib/repository/workspace";
import { createWsStore } from "$lib/stores/util";

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

export function searchTasks(
    sections: WorkspaceBoardSection[],
    searchText: string
): Task[] {
    const tasks: Task[] = lodash.flatten(
        sections.map((section) => (section.tasks ? section.tasks : []))
    );

    const searchEngine = new Fuse<Task>(tasks, {
        keys: ["title"],
        threshold: fuseSearchThreshold,
    });

    return searchEngine
        .search(searchText)
        .map((res: Fuse.FuseResult<Task>) => res.item);
}

export const currentTask = createWsStore<Task>(
    "task",
    currentTaskUuid,
    getTask
);

// XXX Remove the following
import { goto } from "$app/navigation";
import { getDashboardTaskUrl, getDashboardWorkspaceBoardUrl } from "$lib/urls";

export const drawerModalOpen = writable(false);
export const newTaskSectionUuid = writable<string | null>(null);

export function openNewTask(sectionUuid: string): void {
    drawerModalOpen.set(true);
    newTaskSectionUuid.set(sectionUuid);
    currentTaskUuid.set(null);
}
export async function openTaskDetails(
    workspaceBoardUuid: string,
    taskUuid: string,
    subView = "details"
) {
    drawerModalOpen.set(true);
    currentTaskUuid.set(taskUuid);
    await goto(getDashboardTaskUrl(workspaceBoardUuid, taskUuid, subView));
}
export async function closeTaskDetails() {
    drawerModalOpen.set(false);
    currentTaskUuid.set(null);
    const boardUuid = get(currentWorkspaceBoardUuid);
    if (!boardUuid) {
        throw new Error("Expected boardUuid");
    }
    await goto(getDashboardWorkspaceBoardUrl(boardUuid));
}
