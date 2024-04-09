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
import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
import { currentProject } from "$lib/stores/dashboard/project";
import { selectedTeamMember } from "$lib/stores/dashboard/teamMemberFilter";
import type {
    LabelSelection,
    TasksPerUser,
    TeamMemberSelection,
} from "$lib/types/ui";
import type { Label, Task, SectionWithTasks } from "$lib/types/workspace";

interface CurrentFilter {
    labels: LabelSelection;
    teamMember: TeamMemberSelection;
    sections: SectionWithTasks[];
}

function filterSectionsTasks(
    currentFilter: CurrentFilter,
): SectionWithTasks[] {
    let sections: SectionWithTasks[] = currentFilter.sections;
    if (currentFilter.labels.kind === "noLabel") {
        // TODO filter by no label? Justus 2023-04-04
        // eslint-disable-next-line
        // Maybe: return sections;
    } else if (currentFilter.labels.kind === "allLabels") {
        // TODO what to do here?
        // eslint-disable-next-line
        // Maybe: return sections;
    } else {
        const labelUuids = [...currentFilter.labels.labelUuids.keys()];

        sections = sections.map((section) => {
            const tasks = section.tasks.filter((task: Task) => {
                return (
                    task.labels.findIndex((l: Label) =>
                        labelUuids.find((labelUuid) => l.uuid === labelUuid)
                            ? true
                            : false,
                    ) >= 0
                );
            });

            return { ...section, tasks };
        });
    }

    const teamMemberSelection = currentFilter.teamMember;
    if (teamMemberSelection.kind !== "allTeamMembers") {
        sections = sections.map((section) => {
            const tasks = section.tasks.filter((task: Task) => {
                if (teamMemberSelection.kind === "unassigned") {
                    return !task.assignee;
                } else {
                    return task.assignee
                        ? teamMemberSelection.teamMemberUuids.has(
                              task.assignee.uuid,
                          )
                        : false;
                }
            });

            return { ...section, tasks };
        });
    }

    return sections;
}

export const currentSections = derived<
    [typeof selectedLabels, typeof selectedTeamMember, typeof currentProject],
    SectionWithTasks[] | undefined
>(
    [selectedLabels, selectedTeamMember, currentProject],
    ([$selectedLabels, $selectedTeamMember, $currentProject], set) => {
        if (!$currentProject) {
            set(undefined);
            return;
        }
        const sections = $currentProject.sections;
        set(
            filterSectionsTasks({
                labels: $selectedLabels,
                teamMember: $selectedTeamMember,
                sections,
            }),
        );
    },
    undefined,
);

export const tasksPerUser: Readable<TasksPerUser> = derived<
    Readable<SectionWithTasks[] | undefined>,
    TasksPerUser
>(
    currentSections,
    ($currentSections: SectionWithTasks[] | undefined, set) => {
        if ($currentSections === undefined) {
            return;
        }
        const assigned = new Map<string, number>();
        let unassigned = 0;
        $currentSections.forEach((section: SectionWithTasks) => {
            section.tasks.forEach((task) => {
                const uuid = task.assignee?.uuid;
                if (uuid === undefined) {
                    unassigned = unassigned + 1;
                    return;
                }
                const current = assigned.get(uuid) ?? 0;
                assigned.set(uuid, current + 1);
            });
        });
        set({ unassigned, assigned });
    },
    { unassigned: 0, assigned: new Map<string, number>() },
);
