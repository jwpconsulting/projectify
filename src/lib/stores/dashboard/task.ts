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
    searchText: SearchInput,
): TaskWithWorkspaceBoardSection[] {
    const sectionTasks: TaskWithWorkspaceBoardSection[][] = sections.map(
        (workspace_board_section) =>
            (workspace_board_section.tasks ?? []).map((task: Task) => {
                return { ...task, workspace_board_section };
            }),
    );
    const tasks = sectionTasks.flat();
    return searchAmong<TaskWithWorkspaceBoardSection>(
        ["title", "number"],
        tasks,
        searchText,
    );
}

export const currentTask = createWsStore<TaskWithWorkspace>("task", getTask);

export async function deleteTask(task: Task) {
    await repositoryDeleteTask(task);
}
