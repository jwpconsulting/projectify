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
import { getTask } from "$lib/repository/workspace";
import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
import { currentProject } from "$lib/stores/dashboard/project";
import { filterByTeamMember } from "$lib/stores/dashboard/teamMemberFilter";
import { searchAmong } from "$lib/stores/util";
import { createWsStore } from "$lib/stores/wsSubscription";
import type { SearchInput } from "$lib/types/base";
import type {
    // XXX only use TaskWithWorkspace
    TaskWithSection,
    TaskDetail,
    SectionWithTasks,
} from "$lib/types/workspace";

// Clear on project change
// TODO clarify if this subscription still makes sense
// It's good to unsubscribe whenever we can
// Justus 2023-08-30
currentProject.subscribe((_$currentProject) => {
    selectedLabels.set({ kind: "allLabels" });
    filterByTeamMember({ kind: "allTeamMembers" });
});

export function searchTasks(
    sections: readonly SectionWithTasks[],
    searchText: SearchInput,
): readonly TaskWithSection[] {
    type Task = SectionWithTasks["tasks"][number];
    const sectionTasks = sections.map((section) =>
        section.tasks.map((task: Task) => {
            return { ...task, section };
        }),
    );
    const tasks = sectionTasks.flat();
    return searchAmong<TaskWithSection>(
        ["section.title", "title", "number"],
        tasks,
        searchText,
    );
}

export const currentTask = createWsStore<TaskDetail>("task", getTask);
