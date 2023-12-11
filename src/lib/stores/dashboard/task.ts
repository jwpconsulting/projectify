import {
    getTask,
    deleteTask as repositoryDeleteTask,
} from "$lib/repository/workspace";
import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
import { currentWorkspaceBoard } from "$lib/stores/dashboard/workspaceBoard";
import { filterByWorkspaceUser } from "$lib/stores/dashboard/workspaceUserFilter";
import { searchAmong } from "$lib/stores/util";
import { createWsStore } from "$lib/stores/wsSubscription";
import type { SearchInput } from "$lib/types/base";
import type {
    Task,
    // XXX only use TaskWithWorkspace
    TaskWithWorkspaceBoardSection,
    TaskWithWorkspace,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

// Clear on workspace board change
// TODO clarify if this subscription still makes sense
// It's good to unsubscribe whenever we can
// Justus 2023-08-30
currentWorkspaceBoard.subscribe((_$currentWorkspaceBoard) => {
    selectedLabels.set({ kind: "allLabels" });
    filterByWorkspaceUser({ kind: "allWorkspaceUsers" });
});

export function searchTasks(
    sections: WorkspaceBoardSection[],
    searchText: SearchInput
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
